-- Modify "leaderboard_user_stats" table
ALTER TABLE "leaderboard_user_stats" ALTER COLUMN "xp" TYPE bigint, ALTER COLUMN "level" TYPE bigint, ALTER COLUMN "daily_snapshots" TYPE bigint[], ALTER COLUMN "message_count" TYPE bigint, ALTER COLUMN "word_count" TYPE bigint, ALTER COLUMN "attachment_count" TYPE bigint, ALTER COLUMN "explicit_count" TYPE bigint;
