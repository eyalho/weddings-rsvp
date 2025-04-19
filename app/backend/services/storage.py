"""
Storage service module.

Handles persistence of data to various storage backends.
"""
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class DataStorage:
    """
    Service for storing response data.
    
    Handles persistence of message data to various storage backends.
    """
    
    def save_numeric_response(self, message, response_value: str) -> None:
        """
        Save numeric response to CSV file.
        
        Args:
            message: The WhatsApp message
            response_value: The numeric response value
        """
        try:
            # Create data directory if it doesn't exist
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            # Define the CSV file path
            csv_path = data_dir / "numeric_responses.csv"
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
                
            logger.info(f"Saved numeric response to {csv_path}")
        except Exception as e:
            logger.error(f"Failed to save numeric response to CSV: {str(e)}") 