-- Migration: 005_fix_rsvp_statistics_view.sql
-- Description: Fixes the rsvp_statistics view to include an id column
-- PostgreSQL version: 16
-- Depends on: 004_fix_rsvp_guests_schema.sql

-- Begin transaction for safety
BEGIN;

-- Drop the view if it exists
DROP VIEW IF EXISTS rsvp_statistics;

-- Recreate the view with an id column
CREATE OR REPLACE VIEW rsvp_statistics AS
SELECT
    row_number() OVER () AS id,  -- Add this to provide an id for SQLAlchemy
    COUNT(*) AS total_responses,
    COUNT(CASE WHEN rsvp_status = 'confirmed' THEN 1 END) AS attending_count,
    COUNT(CASE WHEN rsvp_status = 'declined' THEN 1 END) AS not_attending_count,
    COALESCE(SUM(CASE WHEN rsvp_status = 'confirmed' THEN COALESCE(num_guests, 1) ELSE 0 END), 0) AS total_guests,
    COALESCE(SUM(CASE WHEN rsvp_status = 'confirmed' THEN COALESCE(num_guests, 1) ELSE 0 END), 0) AS attending_guests,
    COALESCE(SUM(CASE WHEN rsvp_status = 'declined' THEN COALESCE(num_guests, 1) ELSE 0 END), 0) AS not_attending_guests
FROM rsvp_guests;

-- Add comments
COMMENT ON VIEW rsvp_statistics IS 'RSVP statistics view with added id column for ORM compatibility';
COMMENT ON COLUMN rsvp_statistics.id IS 'Synthetic primary key for ORM compatibility';

-- Track this migration in schema_migrations if the table exists
INSERT INTO schema_migrations (migration_name)
SELECT '005_fix_rsvp_statistics_view.sql'
WHERE EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_name = 'schema_migrations'
);

-- Commit the transaction
COMMIT; 