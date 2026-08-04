import { getDb } from "../../../../db";
import { activities, athleteMetrics } from "../../../../db/schema";
import { requireApiUser } from "../../../server/current-user";
import { numberValue, parseCsv } from "../../../server/csv";

async function fingerprint(value: string) {
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(bytes)).map(byte => byte.toString(16).padStart(2, "0")).join("").slice(0, 24);
}

export async function POST(request: Request) {
  try {
    const user = await requireApiUser();
    const form = await request.formData();
    const workouts = form.get("workouts");
    const metrics = form.get("metrics");
    if (!(workouts instanceof File) && !(metrics instanceof File)) {
      return Response.json({ error: "Selecciona workouts.csv o metrics.csv." }, { status: 400 });
    }
    const db = getDb();
    let workoutCount = 0, metricCount = 0;
    if (workouts instanceof File) {
      const rows = parseCsv(await workouts.text());
      for (const row of rows) {
        if (!row.WorkoutDay) continue;
        const startedAt = new Date(`${row.WorkoutDay}T12:00:00Z`);
        const durationSeconds = Math.round(numberValue(row.TimeTotalInHours) * 3600);
        const distanceMeters = Math.round(numberValue(row.DistanceInMeters));
        const trainingStressScore = Math.round(numberValue(row.TSS) * 10) || null;
        if (durationSeconds < 60 && distanceMeters < 100 && !trainingStressScore) continue;
        const externalId = await fingerprint([row.WorkoutDay, row.Title, row.WorkoutType, row.DistanceInMeters, row.TimeTotalInHours].join("|"));
        await db.insert(activities).values({
          userId: user.userId, provider: "trainingpeaks", externalId,
          sportType: row.WorkoutType || "Workout", name: row.Title || row.WorkoutType || "Entrenamiento",
          startedAt, durationSeconds, distanceMeters,
          elevationMeters: null, averageHeartRate: Math.round(numberValue(row.HeartRateAverage)) || null,
          averagePower: Math.round(numberValue(row.PowerAverage)) || null,
          trainingStressScore,
          intensityFactor: Math.round(numberValue(row.IF) * 1000) || null,
          perceivedExertion: Math.round(numberValue(row.Rpe) * 10) || null,
          feeling: Math.round(numberValue(row.Feeling) * 10) || null, syncedAt: new Date(),
        }).onConflictDoUpdate({ target:[activities.provider,activities.externalId], set:{
          durationSeconds,distanceMeters,
          averageHeartRate:Math.round(numberValue(row.HeartRateAverage))||null,averagePower:Math.round(numberValue(row.PowerAverage))||null,
          trainingStressScore,intensityFactor:Math.round(numberValue(row.IF)*1000)||null,syncedAt:new Date(),
        }});
        workoutCount++;
      }
    }
    if (metrics instanceof File) {
      for (const row of parseCsv(await metrics.text())) {
        const measuredAt = new Date(`${row.Timestamp.replace(" ", "T")}Z`);
        if (!row.Type || !Number.isFinite(measuredAt.getTime())) continue;
        await db.insert(athleteMetrics).values({ userId:user.userId,provider:"trainingpeaks",measuredAt,metricType:row.Type,value:Math.round(numberValue(row.Value)*1000) })
          .onConflictDoUpdate({target:[athleteMetrics.userId,athleteMetrics.provider,athleteMetrics.measuredAt,athleteMetrics.metricType],set:{value:Math.round(numberValue(row.Value)*1000)}});
        metricCount++;
      }
    }
    return Response.json({ workouts: workoutCount, metrics: metricCount });
  } catch (error) {
    if (error instanceof Response) return error;
    console.error("TrainingPeaks import failed", error);
    return Response.json({ error: "No fue posible importar los archivos de TrainingPeaks." }, { status: 500 });
  }
}
