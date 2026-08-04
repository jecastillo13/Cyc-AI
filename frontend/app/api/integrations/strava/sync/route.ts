import { and, eq } from "drizzle-orm";
import { getDb } from "../../../../../db";
import { activities, connections } from "../../../../../db/schema";
import { requireApiUser } from "../../../../server/current-user";
import { decryptSecret, encryptSecret } from "../../../../server/secrets";
import { stravaConfig } from "../../../../server/strava-config";
import { analyzeStravaStreams } from "../../../../server/strava-streams";

type StravaActivity = {
  id: number;
  name: string;
  sport_type: string;
  start_date: string;
  elapsed_time: number;
  distance: number;
  total_elevation_gain?: number;
  average_heartrate?: number;
  average_watts?: number;
};

export async function POST() {
  try {
    const user = await requireApiUser();
    const db = getDb();
    const [connection] = await db
      .select()
      .from(connections)
      .where(and(eq(connections.userId, user.userId), eq(connections.provider, "strava")))
      .limit(1);
    if (!connection) return Response.json({ error: "Strava is not connected" }, { status: 404 });

    let accessToken = await decryptSecret(connection.accessTokenEncrypted);
    if (connection.tokenExpiresAt.getTime() <= Date.now() + 3_600_000) {
      const config = stravaConfig();
      const refresh = await fetch("https://www.strava.com/oauth/token", {
        method: "POST",
        headers: { "content-type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: config.clientId,
          client_secret: config.clientSecret,
          grant_type: "refresh_token",
          refresh_token: await decryptSecret(connection.refreshTokenEncrypted),
        }),
      });
      if (!refresh.ok) return Response.json({ error: "Unable to refresh Strava access" }, { status: 502 });
      const token = (await refresh.json()) as {
        access_token: string;
        refresh_token: string;
        expires_at: number;
      };
      accessToken = token.access_token;
      await db
        .update(connections)
        .set({
          accessTokenEncrypted: await encryptSecret(token.access_token),
          refreshTokenEncrypted: await encryptSecret(token.refresh_token),
          tokenExpiresAt: new Date(token.expires_at * 1000),
        })
        .where(eq(connections.id, connection.id));
    }

    const response = await fetch("https://www.strava.com/api/v3/athlete/activities?per_page=100", {
      headers: { authorization: `Bearer ${accessToken}` },
    });
    if (!response.ok) return Response.json({ error: "Unable to read Strava activities" }, { status: 502 });
    const rows = (await response.json()) as StravaActivity[];
    const now = new Date();
    const existing = await db.select({externalId:activities.externalId,streamAnalyzedAt:activities.streamAnalyzedAt}).from(activities).where(and(eq(activities.userId,user.userId),eq(activities.provider,"strava")));
    const analyzed=new Map(existing.map(item=>[item.externalId,item.streamAnalyzedAt]));
    let streamsAnalyzed=0;
    for (const item of rows) {
      await db
        .insert(activities)
        .values({
          userId: user.userId,
          provider: "strava",
          externalId: String(item.id),
          sportType: item.sport_type,
          name: item.name,
          startedAt: new Date(item.start_date),
          durationSeconds: item.elapsed_time,
          distanceMeters: Math.round(item.distance),
          elevationMeters: item.total_elevation_gain ? Math.round(item.total_elevation_gain) : null,
          averageHeartRate: item.average_heartrate ? Math.round(item.average_heartrate) : null,
          averagePower: item.average_watts ? Math.round(item.average_watts) : null,
          syncedAt: now,
        })
        .onConflictDoUpdate({
          target: [activities.provider, activities.externalId],
          set: {
            name: item.name,
            sportType: item.sport_type,
            durationSeconds: item.elapsed_time,
            distanceMeters: Math.round(item.distance),
            syncedAt: now,
          },
        });
      if(!analyzed.get(String(item.id))&&streamsAnalyzed<20){
        const streamResponse=await fetch(`https://www.strava.com/api/v3/activities/${item.id}/streams?keys=time,watts,heartrate,cadence,velocity_smooth,altitude&key_by_type=true`,{headers:{authorization:`Bearer ${accessToken}`}});
        if(streamResponse.ok){const analysis=analyzeStravaStreams(await streamResponse.json() as never);await db.update(activities).set({powerCurve:JSON.stringify(analysis.powerCurve),maxPower:analysis.maxPower||null,maxHeartRate:analysis.maxHeartRate||null,elevationMeters:analysis.elevationMeters||null,powerZones:JSON.stringify(analysis.powerZones),heartRateZones:JSON.stringify(analysis.heartRateZones),streamAnalyzedAt:now}).where(and(eq(activities.userId,user.userId),eq(activities.provider,"strava"),eq(activities.externalId,String(item.id))));streamsAnalyzed++}
      }
    }
    await db.update(connections).set({ lastSyncAt: now }).where(eq(connections.id, connection.id));
    return Response.json({ synced: rows.length, streams_analyzed:streamsAnalyzed });
  } catch (error) {
    if (error instanceof Response) return error;
    return Response.json({ error: "Unable to synchronize Strava" }, { status: 500 });
  }
}
