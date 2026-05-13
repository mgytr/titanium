-- Modify "guild_limits" table
ALTER TABLE "guild_limits" ADD COLUMN "enforcing" boolean NOT NULL DEFAULT true, ADD COLUMN "leaderboard_levels" integer NOT NULL DEFAULT 100, ADD COLUMN "tags" integer NOT NULL DEFAULT 250;
