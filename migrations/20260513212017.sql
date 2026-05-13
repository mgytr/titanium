-- Modify "guild_limits" table
ALTER TABLE "guild_limits" ALTER COLUMN "id" DROP DEFAULT, ADD CONSTRAINT "guild_limits_id_fkey" FOREIGN KEY ("id") REFERENCES "guild_settings" ("guild_id") ON UPDATE NO ACTION ON DELETE CASCADE;
-- Drop sequence used by serial column "id"
DROP SEQUENCE IF EXISTS "guild_limits_id_seq";
