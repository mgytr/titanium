-- Modify "automod_actions" table
ALTER TABLE "automod_actions" DROP CONSTRAINT "automod_actions_guild_id_fkey", ADD CONSTRAINT "automod_actions_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "available_webhooks" table
ALTER TABLE "available_webhooks" ADD CONSTRAINT "available_webhooks_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "error_logs" table
ALTER TABLE "error_logs" ADD CONSTRAINT "error_logs_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "fireboard_messages" table
ALTER TABLE "fireboard_messages" ADD CONSTRAINT "fireboard_messages_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_fireboard_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "guild_prefixes" table
ALTER TABLE "guild_prefixes" ALTER COLUMN "guild_id" DROP DEFAULT, ADD CONSTRAINT "guild_prefixes_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Drop sequence used by serial column "guild_id"
DROP SEQUENCE IF EXISTS "guild_prefixes_guild_id_seq";
-- Modify "leaderboard_user_stats" table
ALTER TABLE "leaderboard_user_stats" ADD CONSTRAINT "leaderboard_user_stats_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_leaderboard_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "mod_case_comments" table
ALTER TABLE "mod_case_comments" ADD CONSTRAINT "mod_case_comments_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Modify "mod_cases" table
ALTER TABLE "mod_cases" ADD CONSTRAINT "mod_cases_guild_id_fkey" FOREIGN KEY ("guild_id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
