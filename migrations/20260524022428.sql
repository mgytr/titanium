-- Modify "guild_settings" table
ALTER TABLE "guild_settings"
ADD COLUMN "prefixes" character varying(5) [] NOT NULL DEFAULT ARRAY ['t!'::character varying];
-- Add prefixes
UPDATE "guild_settings"
SET "prefixes" = gp."prefixes"
FROM "guild_prefixes" gp
WHERE "guild_settings"."guild_id" = gp."guild_id";
-- Drop "guild_prefixes" table
DROP TABLE "guild_prefixes";