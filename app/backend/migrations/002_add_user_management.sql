-- Migration: 002_add_user_management.sql
-- Description: Adds user management and additional tracking capabilities
-- PostgreSQL version: 16
-- Depends on: 001_initial_schema.sql

-- Create users table to store more detailed user information
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE NOT NULL,  -- Primary identifier, must be unique
    name VARCHAR(255),
    email VARCHAR(255),
    rsvp_status VARCHAR(50),                   -- 'confirmed', 'declined', 'pending', etc.
    num_guests INTEGER DEFAULT 0,
    dietary_restrictions TEXT,
    notes TEXT,
    last_interaction_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for users table
CREATE INDEX idx_users_phone_number ON users(phone_number);
CREATE INDEX idx_users_rsvp_status ON users(rsvp_status);
CREATE INDEX idx_users_last_interaction ON users(last_interaction_at);

-- Apply the update timestamp trigger to users table
CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Function to automatically create or update user when a response is received
CREATE OR REPLACE FUNCTION process_user_response() 
RETURNS TRIGGER AS $$
BEGIN
    -- Insert or update user information
    INSERT INTO users (phone_number, name, last_interaction_at)
    VALUES (NEW.phone_number, NEW.profile_name, NOW())
    ON CONFLICT (phone_number) 
    DO UPDATE SET 
        name = COALESCE(EXCLUDED.name, users.name),
        last_interaction_at = NOW(),
        updated_at = NOW();
        
    -- Update RSVP status if this is a button response with specific payloads
    IF NEW.response_type = 'button' THEN
        -- Approve response (payload 1)
        IF NEW.response_data->>'button_payload' = '1' THEN
            UPDATE users 
            SET rsvp_status = 'confirmed'
            WHERE phone_number = NEW.phone_number;
        -- Decline response (payload 2)
        ELSIF NEW.response_data->>'button_payload' = '2' THEN
            UPDATE users 
            SET rsvp_status = 'declined'
            WHERE phone_number = NEW.phone_number;
        -- Not sure yet response (payload 3)
        ELSIF NEW.response_data->>'button_payload' = '3' THEN
            UPDATE users 
            SET rsvp_status = 'pending'
            WHERE phone_number = NEW.phone_number;
        END IF;
    END IF;
    
    -- Handle numeric responses for number of guests
    IF NEW.response_type = 'numeric' THEN
        -- Try to extract numeric value and use it as number of guests
        BEGIN
            UPDATE users 
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

-- Create trigger to process responses and update user information
CREATE TRIGGER process_user_response_trigger
AFTER INSERT ON user_responses
FOR EACH ROW
EXECUTE FUNCTION process_user_response();

-- Create a view for RSVP statistics
CREATE OR REPLACE VIEW rsvp_statistics AS
SELECT
    COUNT(*) AS total_users,
    COUNT(CASE WHEN rsvp_status = 'confirmed' THEN 1 END) AS confirmed_count,
    COUNT(CASE WHEN rsvp_status = 'declined' THEN 1 END) AS declined_count,
    COUNT(CASE WHEN rsvp_status = 'pending' THEN 1 END) AS pending_count,
    COUNT(CASE WHEN rsvp_status IS NULL THEN 1 END) AS unknown_count,
    SUM(COALESCE(num_guests, 0)) AS total_guests
FROM users; 