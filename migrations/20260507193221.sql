-- Modify "tags" table
ALTER TABLE "tags" ADD COLUMN "amount_used" bigint NOT NULL DEFAULT 0;
