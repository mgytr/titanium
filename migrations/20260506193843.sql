-- Modify "guild_settings" table
ALTER TABLE "guild_settings" ADD COLUMN "allow_prefix" boolean NOT NULL DEFAULT true, ADD COLUMN "blocked_channels" bigint[] NOT NULL DEFAULT ARRAY[]::bigint[], ADD COLUMN "blocked_roles" bigint[] NOT NULL DEFAULT ARRAY[]::bigint[];
