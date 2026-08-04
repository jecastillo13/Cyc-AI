ALTER TABLE `activities` ADD `normalized_power` integer;
UPDATE `activities` SET `stream_analyzed_at` = NULL WHERE `provider` = 'strava';
