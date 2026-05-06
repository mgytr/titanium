-- Modify "guild_settings" table
ALTER TABLE "guild_settings" ADD COLUMN "send_not_allowed" boolean NOT NULL DEFAULT true;
