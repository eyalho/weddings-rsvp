"""
Storage service module.

Handles persistence of data to various storage backends.
"""
import csv
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class DataStorage:
    """
    Service for storing response data.
    
    Handles persistence of message data to various storage backends.
    """
    
    def __init__(self, base_dir: str = "data"):
        """
        Initialize the DataStorage service.
        
        Args:
            base_dir: Base directory for storing data files
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
    
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
            # Define the CSV file path for all responses
            csv_path = self.base_dir / "user_responses.csv"
            file_exists = csv_path.exists()
            
            # Define the fields for the CSV
            fields = [
                'timestamp', 
                'phone_number',  # Unique identifier
                'profile_name', 
                'response_type',
                'response_data', 
                'message_sid', 
                'wa_id'
            ]
            
            # Prepare response data as JSON string
            response_json = json.dumps(response_data)
            
            # Open the file in append mode
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                
                # Write header if file doesn't exist
                if not file_exists:
                    writer.writeheader()
                
                # Write the data
                writer.writerow({
                    'timestamp': datetime.now().isoformat(),
                    'phone_number': message.from_number,
                    'profile_name': message.profile_name,
                    'response_type': response_type,
                    'response_data': response_json,
                    'message_sid': message.message_sid,
                    'wa_id': message.wa_id
                })
                
            logger.info(f"Saved {response_type} response from {message.phone_number} to {csv_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save response to CSV: {str(e)}")
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
            # Define the CSV file path
            csv_path = self.base_dir / "user_responses.csv"
            
            # If file doesn't exist, return empty list
            if not csv_path.exists():
                return responses
                
            # Read the CSV file
            with open(csv_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                
                # Filter responses by phone number
                for row in reader:
                    if row['phone_number'] == phone_number:
                        # Parse the JSON response data
                        try:
                            row['response_data'] = json.loads(row['response_data'])
                        except:
                            # If JSON parsing fails, keep as string
                            pass
                            
                        responses.append(row)
            
            logger.info(f"Retrieved {len(responses)} responses for user {phone_number}")
            return responses
            
        except Exception as e:
            logger.error(f"Failed to retrieve user responses: {str(e)}")
            return responses
    
    def save_numeric_response(self, message, response_value: str) -> None:
        """
        Save numeric response to CSV file.
        
        Args:
            message: The WhatsApp message
            response_value: The numeric response value
        """
        # Use the general save_response method with specific response type
        response_data = {'value': response_value}
        self.save_response(message, 'numeric', response_data)
        
        # Also maintain backward compatibility with the old format
        try:
            # Define the CSV file path for numeric responses (legacy)
            csv_path = self.base_dir / "numeric_responses.csv"
            file_exists = csv_path.exists()
            
            # Define the fields for the CSV
            fields = [
                'timestamp', 'phone_number', 'profile_name', 
                'response_value', 'message_sid', 'wa_id'
            ]
            
            # Open the file in append mode
            with open(csv_path, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                
                # Write header if file doesn't exist
                if not file_exists:
                    writer.writeheader()
                
                # Write the data
                writer.writerow({
                    'timestamp': datetime.now().isoformat(),
                    'phone_number': message.from_number,
                    'profile_name': message.profile_name,
                    'response_value': response_value,
                    'message_sid': message.message_sid,
                    'wa_id': message.wa_id
                })
                
            logger.info(f"Saved numeric response to legacy format at {csv_path}")
        except Exception as e:
            logger.error(f"Failed to save numeric response to legacy CSV: {str(e)}")
            
    def save_button_response(self, message, button_text: str, button_payload: str) -> bool:
        """
        Save button response to storage.
        
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