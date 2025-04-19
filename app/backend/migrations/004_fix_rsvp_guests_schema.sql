-- Migration: 004_fix_rsvp_guests_schema.sql
-- Description: Adds the missing user_response_id column to rsvp_guests table
-- PostgreSQL version: 16
-- Depends on: 003_rename_users_to_rsvp_guests.sql

-- Begin transaction for safety
BEGIN;

-- First check if the column already exists
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'rsvp_guests' AND column_name = 'user_response_id'
    ) THEN
        -- Add the missing column - using UUID type to match user_responses.id
        ALTER TABLE rsvp_guests ADD COLUMN user_response_id UUID;
        
        -- Add foreign key constraint if user_responses table exists
        IF EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'user_responses'
        ) THEN
            ALTER TABLE rsvp_guests 
            ADD CONSTRAINT fk_rsvp_guests_user_response 
            FOREIGN KEY (user_response_id) 
            REFERENCES user_responses(id);
        END IF;
        
        -- Log that the column was added
        RAISE NOTICE 'Added user_response_id column to rsvp_guests table';
    ELSE
        -- Log that the column already exists
        RAISE NOTICE 'Column user_response_id already exists in rsvp_guests table';
    END IF;
END $$;

-- Track this migration in schema_migrations if the table exists
INSERT INTO schema_migrations (migration_name)
SELECT '004_fix_rsvp_guests_schema.sql'
WHERE EXISTS (
    SELECT 1 
    FROM information_schema.tables 
    WHERE table_name = 'schema_migrations'
);

-- Commit the transaction
COMMIT; 