-- Modify "guild_leaderboard_settings" table
ALTER TABLE "guild_leaderboard_settings"
ALTER COLUMN "web_login_required"
SET DEFAULT true;
-- Set previous entries to true as well
UPDATE "guild_leaderboard_settings"
SET web_login_required = true;