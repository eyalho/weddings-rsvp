"""
Storage service module.

Handles persistence of data to PostgreSQL database.
"""
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import psycopg2
from psycopg2.extras import RealDictCursor, Json

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class DataStorage:
    """
    Service for storing response data.
    
    Handles persistence of message data to PostgreSQL database.
    """
    
    def __init__(self, db_uri: Optional[str] = None):
        """
        Initialize the DataStorage service.
        
        Args:
            db_uri: PostgreSQL connection URI. If None, uses environment variable.
        """
        # Get database URI from environment variable if not provided
        self.db_uri = db_uri or os.environ.get(
            "DATABASE_URL",
            "postgresql://eyalh:ddDYj6p4bJObufNKFGq4qhqvOwVelBQ4@dpg-d01p48buibrs73b1ht40-a/rsvp_4sgh"
        )
        self._test_connection()
    
    def _test_connection(self):
        """Test the database connection and log the result."""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    logger.info(f"Connected to PostgreSQL. Version: {version}")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
            
    def _get_connection(self):
        """Get a PostgreSQL connection."""
        return psycopg2.connect(self.db_uri)
    
    def save_response(self, message, response_type: str, response_data: Dict[str, Any]) -> bool:
        """
        Save any type of user response with phone_number as unique identifier.
        
        Args:
            message: The WhatsApp message
            response_type: Type of response (e.g., 'button', 'numeric', 'general')
            response_data: Additional data about the response
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # Insert into user_responses table
                    cursor.execute(
                        """
                        INSERT INTO user_responses 
                        (phone_number, profile_name, response_type, response_data, 
                        message_sid, wa_id, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            message.from_number,
                            message.profile_name,
                            response_type,
                            Json(response_data),
                            message.message_sid,
                            message.wa_id,
                            datetime.now()
                        )
                    )
                    
            logger.info(f"Saved {response_type} response from {message.from_number} to database")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save response to database: {str(e)}")
            return False
            
    def get_user_responses(self, phone_number: str) -> List[Dict[str, Any]]:
        """
        Retrieve all responses for a specific user by phone number.
        
        Args:
            phone_number: Phone number as unique identifier
            
        Returns:
            List of response records for the user
        """
        responses = []
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM user_responses
                        WHERE phone_number = %s
                        ORDER BY created_at DESC
                        """,
                        (phone_number,)
                    )
                    responses = cursor.fetchall()
            
            # Convert responses to list of dictionaries
            result = [dict(row) for row in responses]
            logger.info(f"Retrieved {len(result)} responses for user {phone_number}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve user responses: {str(e)}")
            return []
    
    def save_numeric_response(self, message, response_value: str) -> None:
        """
        Save numeric response to database.
        
        Args:
            message: The WhatsApp message
            response_value: The numeric response value
        """
        # Use the general save_response method with specific response type
        response_data = {'value': response_value}
        self.save_response(message, 'numeric', response_data)
            
    def save_button_response(self, message, button_text: str, button_payload: str) -> bool:
        """
        Save button response to database.
        
        Args:
            message: The WhatsApp message
            button_text: Text displayed on the button
            button_payload: Payload data from the button
            
        Returns:
            True if successful, False otherwise
        """
        response_data = {
            'button_text': button_text,
            'button_payload': button_payload
        }
        return self.save_response(message, 'button', response_data)
        
    def get_latest_user_response(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest response from a user.
        
        Args:
            phone_number: The user's phone number
            
        Returns:
            The latest response or None if no responses exist
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM user_responses
                        WHERE phone_number = %s
                        ORDER BY created_at DESC
                        LIMIT 1
                        """,
                        (phone_number,)
                    )
                    response = cursor.fetchone()
                    
            if response:
                return dict(response)
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve latest user response: {str(e)}")
            return None
    
    def get_responses_by_type(self, response_type: str) -> List[Dict[str, Any]]:
        """
        Get all responses of a specific type.
        
        Args:
            response_type: The type of responses to retrieve
            
        Returns:
            List of responses
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT * FROM user_responses
                        WHERE response_type = %s
                        ORDER BY created_at DESC
                        """,
                        (response_type,)
                    )
                    responses = cursor.fetchall()
                    
            result = [dict(row) for row in responses]
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve responses by type: {str(e)}")
            return []
    
    def get_rsvp_status(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """
        Get RSVP status for a specific guest by phone number.
        
        Args:
            phone_number: Phone number as unique identifier
            
        Returns:
            Dictionary with RSVP information or None if not found
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT id, phone_number, name, rsvp_status, num_guests, 
                               dietary_restrictions, last_interaction_at
                        FROM rsvp_guests
                        WHERE phone_number = %s
                        """,
                        (phone_number,)
                    )
                    result = cursor.fetchone()
                    
            if result:
                return dict(result)
            return None
            
        except Exception as e:
            logger.error(f"Failed to retrieve RSVP status: {str(e)}")
            return None
            
    def update_rsvp_details(self, phone_number: str, updates: Dict[str, Any]) -> bool:
        """
        Update RSVP details for a guest.
        
        Args:
            phone_number: Phone number as unique identifier
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        if not updates:
            return True
            
        try:
            # Build the SET clause dynamically
            set_clause_parts = []
            params = []
            
            for field, value in updates.items():
                set_clause_parts.append(f"{field} = %s")
                params.append(value)
            
            # Add the phone_number to the parameters
            params.append(phone_number)
            
            set_clause = ", ".join(set_clause_parts)
            
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"""
                        UPDATE rsvp_guests
                        SET {set_clause}
                        WHERE phone_number = %s
                        """,
                        params
                    )
                    
            logger.info(f"Updated RSVP details for {phone_number}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update RSVP details: {str(e)}")
            return False
    
    def get_rsvp_statistics(self) -> Dict[str, int]:
        """
        Get overall RSVP statistics.
        
        Returns:
            Dictionary with RSVP statistics
        """
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("SELECT * FROM rsvp_statistics")
                    result = cursor.fetchone()
                    
            if result:
                return dict(result)
            return {
                "total_guests": 0,
                "confirmed_count": 0,
                "declined_count": 0,
                "pending_count": 0,
                "unknown_count": 0,
                "total_attendees": 0
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve RSVP statistics: {str(e)}")
            return {
                "total_guests": 0,
                "confirmed_count": 0,
                "declined_count": 0,
                "pending_count": 0,
                "unknown_count": 0,
                "total_attendees": 0
            } 