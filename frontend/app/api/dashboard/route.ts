import { and, asc, eq, gte } from "drizzle-orm";
import { getDb } from "../../../db";
import { activities } from "../../../db/schema";
import { requireApiUser } from "../../server/current-user";

const DAY_MS = 86_400_000;

function dayKey(value: Date) {
  return value.toISOString().slice(0, 10);
}

function round(value: number, digits = 1) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function exponentialLoad(loads: number[], timeConstant: number) {
  const alpha = 1 - Math.exp(-1 / timeConstant);
  return loads.reduce((current, load) => current + alpha * (load - current), 0);
}

type ActivityRow = {
  provider:string;name:string;sportType:string;startedAt:Date;durationSeconds:number;distanceMeters:number;
  elevationMeters:number|null;trainingStressScore:number|null;intensityFactor:number|null;
};

function sameWorkout(left: ActivityRow, right: ActivityRow) {
  if (Math.abs(left.startedAt.getTime() - right.startedAt.getTime()) > 18 * 3_600_000) return false;
  const durationClose = left.durationSeconds > 0 && right.durationSeconds > 0 && Math.abs(left.durationSeconds-right.durationSeconds)/Math.max(left.durationSeconds,right.durationSeconds) <= .15;
  const hasDistances = left.distanceMeters > 500 && right.distanceMeters > 500;
  const distanceClose = hasDistances && Math.abs(left.distanceMeters-right.distanceMeters)/Math.max(left.distanceMeters,right.distanceMeters) <= .08;
  return durationClose && (!hasDistances || distanceClose);
}

function cleanAndDedupe(rows: ActivityRow[]) {
  const valid = rows.filter(row => row.durationSeconds >= 60 || row.distanceMeters >= 100 || (row.trainingStressScore || 0) > 0);
  return valid.reduce<ActivityRow[]>((result, row) => {
    const match = result.findIndex(existing => existing.provider !== row.provider && sameWorkout(existing, row));
    if (match < 0) result.push(row);
    else if (row.provider === "trainingpeaks" && row.trainingStressScore) result[match] = { ...result[match], ...row, elevationMeters: row.elevationMeters || result[match].elevationMeters };
    return result;
  }, []);
}

export async function GET() {
  try {
    const user = await requireApiUser();
    const now = new Date();
    const today = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
    const start = new Date(today.getTime() - 89 * DAY_MS);
    const rawRows = await getDb()
      .select({
        provider: activities.provider,
        name: activities.name,
        sportType: activities.sportType,
        startedAt: activities.startedAt,
        durationSeconds: activities.durationSeconds,
        distanceMeters: activities.distanceMeters,
        elevationMeters: activities.elevationMeters,
        trainingStressScore: activities.trainingStressScore,
        intensityFactor: activities.intensityFactor,
      })
      .from(activities)
      .where(andUserAndDate(user.userId, start))
      .orderBy(asc(activities.startedAt));
    const rows = cleanAndDedupe(rawRows);

    const daily = new Map<string, number>();
    for (const row of rows) {
      // Until power/heart-rate zones are available, moving minutes are used as
      // a transparent training-load estimate. The physiological model can
      // later replace this with TSS/TRIMP without changing the API contract.
      const estimatedLoad = row.trainingStressScore ? row.trainingStressScore / 10 : Math.max(0, row.durationSeconds / 60);
      const key = dayKey(row.startedAt);
      daily.set(key, (daily.get(key) || 0) + estimatedLoad);
    }

    const series = Array.from({ length: 90 }, (_, index) => {
      const date = new Date(start.getTime() + index * DAY_MS);
      const dateKey = dayKey(date);
      return { date: dateKey, load: round(daily.get(dateKey) || 0) };
    });
    const loads = series.map((point) => point.load);
    const atl = exponentialLoad(loads, 7);
    const ctl = exponentialLoad(loads, 42);
    const tsb = ctl - atl;
    const fatigue = ctl > 0 ? Math.min(100, Math.max(0, (atl / ctl) * 50 + (tsb < 0 ? Math.min(-tsb, 50) : 0))) : 0;
    const recovery = Math.min(100, Math.max(0, 100 - fatigue + Math.min(15, Math.max(-15, tsb))));

    const weekStart = new Date(today.getTime() - 6 * DAY_MS);
    const previousWeekStart = new Date(today.getTime() - 13 * DAY_MS);
    const currentRows = rows.filter((row) => row.startedAt >= weekStart);
    const previousRows = rows.filter((row) => row.startedAt >= previousWeekStart && row.startedAt < weekStart);
    const activityLoad = (row:ActivityRow) => row.trainingStressScore ? row.trainingStressScore / 10 : row.durationSeconds / 60;
    const currentLoad = currentRows.reduce((total, row) => total + activityLoad(row), 0);
    const previousLoad = previousRows.reduce((total, row) => total + activityLoad(row), 0);
    const loadTrend = previousLoad > 0 ? ((currentLoad - previousLoad) / previousLoad) * 100 : currentLoad > 0 ? 100 : 0;

    return Response.json({
      athlete: { name: user.displayName },
      history: {
        workouts_last_7_days: currentRows.length,
        distance_last_7_days: round(currentRows.reduce((total, row) => total + row.distanceMeters, 0) / 1000),
        duration_hours_last_7_days: round(currentRows.reduce((total, row) => total + row.durationSeconds, 0) / 3600),
        elevation_last_7_days: Math.round(currentRows.reduce((total, row) => total + (row.elevationMeters || 0), 0)),
        load_trend_percent: round(loadTrend),
      },
      training_status: {
        atl: round(atl),
        ctl: round(ctl),
        tsb: round(tsb),
        fatigue_score: round(fatigue),
        recovery_score: round(recovery),
        fitness_score: round(Math.min(100, Math.max(0, ctl))),
        readiness: recovery >= 70 ? "high" : recovery >= 40 ? "moderate" : "low",
        injury_risk: fatigue >= 80 || tsb <= -25 ? "high" : fatigue >= 60 || tsb <= -10 ? "moderate" : "low",
      },
      charts: { daily_load: series.slice(-28) },
      recent_activities: rows.slice(-5).reverse().map((row) => ({
        name: row.name,
        sport_type: row.sportType,
        date: row.startedAt.toISOString(),
        duration_minutes: Math.round(row.durationSeconds / 60),
        distance_km: round(row.distanceMeters / 1000),
        elevation_meters: row.elevationMeters || 0,
        tss: row.trainingStressScore ? row.trainingStressScore / 10 : null,
        intensity_factor: row.intensityFactor ? row.intensityFactor / 1000 : null,
      })),
    });
  } catch (error) {
    if (error instanceof Response) return error;
    console.error("Dashboard calculation failed", error);
    return Response.json({ error: "Unable to calculate dashboard" }, { status: 500 });
  }
}

function andUserAndDate(userId: string, start: Date) {
  return and(eq(activities.userId, userId), gte(activities.startedAt, start));
}
