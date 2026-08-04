ALTER TABLE `activities` ADD `training_stress_score` integer;
ALTER TABLE `activities` ADD `intensity_factor` integer;
ALTER TABLE `activities` ADD `perceived_exertion` integer;
ALTER TABLE `activities` ADD `feeling` integer;
CREATE TABLE `athlete_metrics` (
  `id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
  `user_id` text NOT NULL,
  `provider` text NOT NULL,
  `measured_at` integer NOT NULL,
  `metric_type` text NOT NULL,
  `value` integer NOT NULL,
  FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON UPDATE no action ON DELETE cascade
);
CREATE UNIQUE INDEX `idx_metrics_user_provider_date_type` ON `athlete_metrics` (`user_id`,`provider`,`measured_at`,`metric_type`);
