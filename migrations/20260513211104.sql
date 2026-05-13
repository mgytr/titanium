-- Modify "guild_limits" table
ALTER TABLE "guild_limits" ALTER COLUMN "bad_word_list_size" SET DEFAULT 1000;
-- Change old limit to new limit
UPDATE guild_limits SET bad_word_list_size = 1000 WHERE bad_word_list_size = 1500;