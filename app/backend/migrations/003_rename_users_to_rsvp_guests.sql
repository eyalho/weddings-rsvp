-- Migration: 003_rename_users_to_rsvp_guests.sql
-- Description: Renames the users table to rsvp_guests to better reflect its purpose
-- PostgreSQL version: 16
-- Depends on: 002_add_user_management.sql

-- Begin transaction for safety
BEGIN;

-- First, drop dependent objects that reference the users table
DROP VIEW IF EXISTS rsvp_statistics;
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP TRIGGER IF EXISTS process_user_response_trigger ON user_responses;
DROP FUNCTION IF EXISTS process_user_response();

-- Rename the table
ALTER TABLE IF EXISTS users RENAME TO rsvp_guests;

-- Rename indexes
ALTER INDEX IF EXISTS idx_users_phone_number RENAME TO idx_rsvp_guests_phone_number;
ALTER INDEX IF EXISTS idx_users_rsvp_status RENAME TO idx_rsvp_guests_rsvp_status;
ALTER INDEX IF EXISTS idx_users_last_interaction RENAME TO idx_rsvp_guests_last_interaction;

-- Recreate the trigger on the renamed table
CREATE TRIGGER update_rsvp_guests_updated_at
BEFORE UPDATE ON rsvp_guests
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Recreate the function with updated table references
CREATE OR REPLACE FUNCTION process_user_response() 
RETURNS TRIGGER AS $$
BEGIN
    -- Insert or update guest information
    INSERT INTO rsvp_guests (phone_number, name, last_interaction_at)
    VALUES (NEW.phone_number, NEW.profile_name, NOW())
    ON CONFLICT (phone_number) 
    DO UPDATE SET 
        name = COALESCE(EXCLUDED.name, rsvp_guests.name),
        last_interaction_at = NOW(),
        updated_at = NOW();
        
    -- Update RSVP status if this is a button response with specific payloads
    IF NEW.response_type = 'button' THEN
        -- Approve response (payload 1)
        IF NEW.response_data->>'button_payload' = '1' THEN
            UPDATE rsvp_guests 
            SET rsvp_status = 'confirmed'
            WHERE phone_number = NEW.phone_number;
        -- Decline response (payload 2)
        ELSIF NEW.response_data->>'button_payload' = '2' THEN
            UPDATE rsvp_guests 
            SET rsvp_status = 'declined'
            WHERE phone_number = NEW.phone_number;
        -- Not sure yet response (payload 3)
        ELSIF NEW.response_data->>'button_payload' = '3' THEN
            UPDATE rsvp_guests 
            SET rsvp_status = 'pending'
            WHERE phone_number = NEW.phone_number;
        END IF;
    END IF;
    
    -- Handle numeric responses for number of guests
    IF NEW.response_type = 'numeric' THEN
        -- Try to extract numeric value and use it as number of guests
        BEGIN
            UPDATE rsvp_guests 
            SET num_guests = (NEW.response_data->>'value')::integer
            WHERE phone_number = NEW.phone_number;
        EXCEPTION WHEN OTHERS THEN
            -- Ignore if not a valid number
            NULL;
        END;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Recreate the trigger on user_responses
CREATE TRIGGER process_user_response_trigger
AFTER INSERT ON user_responses
FOR EACH ROW
EXECUTE FUNCTION process_user_response();

-- Recreate the view using the renamed table
CREATE OR REPLACE VIEW rsvp_statistics AS
SELECT
    COUNT(*) AS total_guests,
    COUNT(CASE WHEN rsvp_status = 'confirmed' THEN 1 END) AS confirmed_count,
    COUNT(CASE WHEN rsvp_status = 'declined' THEN 1 END) AS declined_count,
    COUNT(CASE WHEN rsvp_status = 'pending' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN rsvp_status IS NULL THEN 1 END) AS unknown_count,
    SUM(COALESCE(num_guests, 0)) AS total_attendees
FROM rsvp_guests;

-- Add comments to the new objects
COMMENT ON TABLE rsvp_guests IS 'Stores consolidated guest information and RSVP status';
COMMENT ON COLUMN rsvp_guests.phone_number IS 'Guest phone number - primary identifier for the guest';
COMMENT ON COLUMN rsvp_guests.rsvp_status IS 'RSVP status (confirmed, declined, pending)';
COMMENT ON COLUMN rsvp_guests.num_guests IS 'Number of guests attending with the primary guest';

-- Update migration tracking to avoid confusion
UPDATE schema_migrations 
SET migration_name = '002_add_guest_management.sql' 
WHERE migration_name = '002_add_user_management.sql';

-- Commit the transaction
COMMIT; 