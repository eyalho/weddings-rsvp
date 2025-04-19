-- Migration: 006_add_attending_column.sql
-- Description: Adds the attending column to rsvp_guests table
-- PostgreSQL version: 16
-- Depends on: 005_fix_rsvp_statistics_view.sql

-- Begin transaction for safety
BEGIN;

-- First check if the column already exists
DO $$
BEGIN
    -- Check if the attending column exists
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'rsvp_guests' AND column_name = 'attending'
    ) THEN
        -- Add the attending column
        ALTER TABLE rsvp_guests ADD COLUMN attending BOOLEAN DEFAULT FALSE;
        
        -- If rsvp_status column exists, populate attending based on it
        IF EXISTS (
            SELECT 1 
            FROM information_schema.columns 
            WHERE table_name = 'rsvp_guests' AND column_name = 'rsvp_status'
        ) THEN
            -- Update attending based on rsvp_status
            UPDATE rsvp_guests 
            SET attending = CASE 
                WHEN rsvp_status = 'confirmed' THEN TRUE 
                ELSE FALSE 
            END;
        END IF;
        
        RAISE NOTICE 'Added attending column to rsvp_guests table';
    ELSE
        RAISE NOTICE 'Column attending already exists in rsvp_guests table';
    END IF;
END $$;

-- Make sure dietary_restrictions column exists as well
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'rsvp_guests' AND column_name = 'dietary_restrictions'
    ) THEN
        ALTER TABLE rsvp_guests ADD COLUMN dietary_restrictions TEXT;
        RAISE NOTICE 'Added dietary_restrictions column to rsvp_guests table';
    ELSE
        RAISE NOTICE 'Column dietary_restrictions already exists in rsvp_guests table';
    END IF;
END $$;

-- Track this migration in schema_migrations if the table exists
INSERT INTO schema_migrations (migration_name)
SELECT '006_add_attending_column.sql'
WHERE EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_name = 'schema_migrations'
);

-- Commit the transaction
COMMIT; 