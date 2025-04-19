-- Migration: 001_initial_schema.sql
-- Description: Creates the initial database schema for the RSVP system
-- PostgreSQL version: 16

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create user_responses table
CREATE TABLE IF NOT EXISTS user_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) NOT NULL,  -- Unique identifier for the user
    profile_name VARCHAR(255),
    response_type VARCHAR(50) NOT NULL, -- Type of response (button, numeric, etc.)
    response_data JSONB NOT NULL,       -- Flexible storage for response details
    message_sid VARCHAR(50),            -- Twilio message SID
    wa_id VARCHAR(50),                  -- WhatsApp ID
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for faster queries
CREATE INDEX idx_user_responses_phone_number ON user_responses(phone_number);
CREATE INDEX idx_user_responses_response_type ON user_responses(response_type);
CREATE INDEX idx_user_responses_created_at ON user_responses(created_at);

-- For efficient querying of the JSONB data
CREATE INDEX idx_user_responses_response_data ON user_responses USING GIN (response_data);

-- Create a simple trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to user_responses table
CREATE TRIGGER update_user_responses_updated_at
BEFORE UPDATE ON user_responses
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Create a view for easy access to button responses
CREATE VIEW button_responses AS
SELECT 
    id,
    phone_number,
    profile_name,
    response_data->>'button_text' AS button_text,
    response_data->>'button_payload' AS button_payload,
    created_at
FROM user_responses
WHERE response_type = 'button';

-- Create a view for easy access to numeric responses
CREATE VIEW numeric_responses AS
SELECT 
    id,
    phone_number,
    profile_name,
    response_data->>'value' AS numeric_value,
    created_at
FROM user_responses
WHERE response_type = 'numeric';

-- Comment on tables and columns for documentation
COMMENT ON TABLE user_responses IS 'Stores all user responses from WhatsApp interactions';
COMMENT ON COLUMN user_responses.phone_number IS 'User phone number - primary identifier for the user';
COMMENT ON COLUMN user_responses.response_type IS 'Type of response (button, numeric, text, etc.)';
COMMENT ON COLUMN user_responses.response_data IS 'JSON data containing the details of the response'; 