import { integer, sqliteTable, text, uniqueIndex } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  displayName: text("display_name").notNull(),
  passwordHash: text("password_hash").notNull(),
  createdAt: integer("created_at", { mode: "timestamp_ms" }).notNull(),
  updatedAt: integer("updated_at", { mode: "timestamp_ms" }).notNull(),
});

export const sessions = sqliteTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  tokenHash: text("token_hash").notNull().unique(),
  expiresAt: integer("expires_at", { mode: "timestamp_ms" }).notNull(),
  createdAt: integer("created_at", { mode: "timestamp_ms" }).notNull(),
});

export const connections = sqliteTable("connections", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  provider: text("provider").notNull(),
  providerUserId: text("provider_user_id").notNull(),
  displayName: text("display_name"),
  scopes: text("scopes").notNull(),
  accessTokenEncrypted: text("access_token_encrypted").notNull(),
  refreshTokenEncrypted: text("refresh_token_encrypted").notNull(),
  tokenExpiresAt: integer("token_expires_at", { mode: "timestamp_ms" }).notNull(),
  connectedAt: integer("connected_at", { mode: "timestamp_ms" }).notNull(),
  lastSyncAt: integer("last_sync_at", { mode: "timestamp_ms" }),
}, table => [uniqueIndex("idx_connections_user_provider").on(table.userId, table.provider)]);

export const activities = sqliteTable("activities", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  provider: text("provider").notNull(),
  externalId: text("external_id").notNull(),
  sportType: text("sport_type").notNull(),
  name: text("name").notNull(),
  startedAt: integer("started_at", { mode: "timestamp_ms" }).notNull(),
  durationSeconds: integer("duration_seconds").notNull(),
  distanceMeters: integer("distance_meters").notNull(),
  elevationMeters: integer("elevation_meters"),
  averageHeartRate: integer("average_heart_rate"),
  averagePower: integer("average_power"),
  maxHeartRate: integer("max_heart_rate"),
  maxPower: integer("max_power"),
  averageCadence: integer("average_cadence"),
  energyKj: integer("energy_kj"),
  plannedDurationSeconds: integer("planned_duration_seconds"),
  plannedDistanceMeters: integer("planned_distance_meters"),
  heartRateZones: text("heart_rate_zones"),
  powerZones: text("power_zones"),
  powerCurve: text("power_curve"),
  streamAnalyzedAt: integer("stream_analyzed_at", { mode: "timestamp_ms" }),
  trainingStressScore: integer("training_stress_score"),
  intensityFactor: integer("intensity_factor"),
  perceivedExertion: integer("perceived_exertion"),
  feeling: integer("feeling"),
  syncedAt: integer("synced_at", { mode: "timestamp_ms" }).notNull(),
}, table => [uniqueIndex("idx_activities_provider_external").on(table.provider, table.externalId)]);

export const athleteMetrics = sqliteTable("athlete_metrics", {
  id: integer("id").primaryKey({ autoIncrement: true }),
  userId: text("user_id").notNull().references(() => users.id, { onDelete: "cascade" }),
  provider: text("provider").notNull(),
  measuredAt: integer("measured_at", { mode: "timestamp_ms" }).notNull(),
  metricType: text("metric_type").notNull(),
  value: integer("value").notNull(),
}, table => [uniqueIndex("idx_metrics_user_provider_date_type").on(table.userId, table.provider, table.measuredAt, table.metricType)]);
