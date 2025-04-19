"""
Webhook service module.

Handles webhook data processing following:
- "Simple is better than complex"
- "Explicit is better than implicit"
- "Readability counts"
"""
import json
import logging
import os
import re
import csv
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass
from pathlib import Path

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """
    Explicit message type enumeration.
    
    Makes valid message types explicit rather than using magic strings.
    """
    GREETING = "greeting"
    RSVP = "rsvp"
    QUESTION = "question"
    MEDIA = "media"
    GENERAL = "general"
    BUTTON = "button"
    NUMERIC = "numeric"
    UNKNOWN = "unknown"


@dataclass
class WhatsAppMessage:
    """
    WhatsApp message data structure.
    
    Using dataclass makes the structure explicit and self-documenting.
    """
    message_sid: str
    from_number: str
    to_number: str
    profile_name: str
    body: str
    num_media: str
    status: str
    wa_id: str
    # Button interaction fields
    message_type: str = ""
    button_text: str = ""
    button_payload: str = ""
    original_replied_message_sid: str = ""
    original_replied_message_sender: str = ""
    media: Optional[List[Dict[str, str]]] = None


class WebhookService:
    """
    Service for processing webhook data.
    
    Using a class with explicit methods makes the responsibilities
    clear and follows good OOP design.
    """
    
    def process_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook data.
        
        Simple, focused method that delegates to appropriate handlers
        based on message type.
        
        Args:
            data: The webhook payload
            
        Returns:
            Response data
        """
        # Log what we're processing - be explicit
        webhook_type = data.get('type', 'unknown')
        logger.info(f"Processing webhook data type: {webhook_type}")
        
        # Debug log to see exact data structure
        logger.debug(f"Data type: {type(data)}, Keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        logger.debug(f"Type check: type={webhook_type}, is 'whatsapp'={webhook_type == 'whatsapp'}, has 'message'={'message' in data}")
        
        # Handle empty data
        if not data or (isinstance(data, dict) and len(data) == 0) or (isinstance(data, str) and not data.strip()):
            return {"status": "webhook processed", "message": "Empty request", "type": "empty"}
            
        # Simple logging of payload details
        logger.info(f"Generic webhook payload: {json.dumps(data, indent=2, default=str)}")
        
        # Simple, consistent response matching test expectations
        return {"status": "webhook processed", "type": "generic"}
    
    def handle_whatsapp_message(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle a WhatsApp message.
        Simple method that categorizes messages and returns appropriate responses.
        Args:
            message: The WhatsApp message data as a WhatsAppMessage object
        Returns:
            Response data with message type
        """
        # Log what we're processing
        logger.info(f"Processing WhatsApp message from {message.profile_name}")
        
        # Determine message type - explicit categorization
        message_type = self._categorize_message(message)
        
        # Log the categorization
        logger.info(
            f"Message from {message.from_number} categorized as {message_type}"
        )
        
        # Handle different message types
        if message_type == MessageType.BUTTON:
            return self._handle_button_response(message)
        elif message_type == MessageType.NUMERIC:
            return self._handle_numeric_response(message)
        
        # Here you would typically store the message in a database
        # self.save_message(message, message_type)
        
        # Return a simple, consistent response matching test expectations
        return {
            "status": "whatsapp_message_processed",
            "message_type": message_type,
            "from": message.from_number
        }
    
    def _handle_button_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle button response based on button text and payload.
        
        Args:
            message: The WhatsApp message with button interaction
            
        Returns:
            Response data specific to the button interaction
        """
        logger.info(f"Handling button response: {message.button_text} (payload: {message.button_payload})")
        
        # Handle specific button responses
        if message.button_text == "לצערי לא" and message.button_payload == "2":
            # Custom response for "Unfortunately not" button with payload 2
            return self._handle_decline_response(message)
        elif message.button_text == "כן, אגיע!" and message.button_payload == "1":
            # Custom response for approval button
            return self._handle_approve_response(message)
        elif message.button_text == "עוד לא יודע/ת" and message.button_payload == "3":
            # Custom response for "Don't know yet" button 
            return self._handle_not_know_yet_response(message)
            
        # Default button response
        return {
            "status": "button_response_processed",
            "message_type": MessageType.BUTTON,
            "button_text": message.button_text,
            "button_payload": message.button_payload,
            "from": message.from_number
        }
    
    def _send_twilio_template(self, message: WhatsAppMessage, template_sid: str, additional_data: Dict = None) -> Dict[str, Any]:
        """
        Core method to send Twilio templates - reduces code duplication.
        
        Args:
            message: The WhatsApp message to respond to
            template_sid: The Twilio template SID to use
            additional_data: Any additional data to include in the response
            
        Returns:
            Response data with Twilio status
        """
        import os
        import json
        from twilio.rest import Client
        from twilio.base.exceptions import TwilioRestException
        
        # Base response data
        response = {
            "status": "response_processed",
            "message_type": MessageType.BUTTON,
            "from": message.from_number
        }
        
        # Add any additional data
        if additional_data:
            response.update(additional_data)
        
        # Set Twilio credentials - retrieve from environment variables
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        
        # Validate credentials are available
        if not account_sid or not auth_token:
            error_msg = "Twilio credentials not properly configured. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables."
            logger.error(error_msg)
            response["twilio_status"] = "error"
            response["twilio_error"] = error_msg
            return response
            
        client = Client(account_sid, auth_token)
        
        # WhatsApp config
        from_number = "whatsapp:+972509518554"
        
        # Extract guest info from the message
        guest_name = message.profile_name
        phone_number = message.from_number
        
        # Phone validation
        def is_valid_phone(number: str) -> bool:
            return re.match(r"^\+\d{10,15}$", number) is not None
        
        # Build WhatsApp template variables
        def build_template_vars(name, phone):
            date = "April 20th"
            rsvp_link = f"https://rsvp.link/{phone[-4:]}"
            return {
                "1": name,
                "2": date,
                "3": rsvp_link
            }
        
        try:
            # Ensure phone is in correct format
            if not phone_number.startswith("+"):
                phone_number = "+" + phone_number
                
            if not is_valid_phone(phone_number):
                logger.error(f"Invalid phone number format: {phone_number}")
                response["twilio_status"] = "error"
                response["twilio_error"] = f"Invalid phone number format: {phone_number}"
                return response
            
            # Send message
            vars = build_template_vars(guest_name, phone_number)
            twilio_message = client.messages.create(
                from_=from_number,
                to=f"whatsapp:{phone_number}",
                content_sid=template_sid,
                content_variables=json.dumps(vars)
            )
            logger.info(f"Sent to {phone_number} | SID: {twilio_message.sid}")
            
            # Check delivery status
            message_status = client.messages(twilio_message.sid).fetch().status
            logger.info(f"Message status: {message_status}")
            
            # Add Twilio info to response
            response["twilio_status"] = message_status
            response["twilio_message_sid"] = twilio_message.sid
            
        except TwilioRestException as e:
            error_msg = f"Failed to send message via Twilio: {str(e)}"
            logger.error(error_msg)
            
            # Check for authentication errors
            if e.code == 20003 or "401" in str(e):
                auth_error = "Twilio authentication failed. Please verify your TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables."
                logger.error(auth_error)
                response["twilio_status"] = "auth_error"
                response["twilio_error"] = auth_error
            else:
                response["twilio_status"] = "error"
                response["twilio_error"] = error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error sending Twilio message: {str(e)}"
            logger.error(error_msg)
            response["twilio_status"] = "error"
            response["twilio_error"] = error_msg
            
        return response
    
    def _handle_decline_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle decline response (לצערי לא - Unfortunately not).
        Send a follow-up message using Twilio API.
        
        Args:
            message: The WhatsApp message with decline button interaction
            
        Returns:
            Response data for decline interaction
        """
        logger.info(f"Handling decline response from {message.profile_name}")
        
        # Use the shared template sending method with decline-specific template
        template_sid = "HXbfc74d3f86589ff6553694987fe72c99"
        return self._send_twilio_template(
            message, 
            template_sid,
            {"response_type": "decline"}
        )
    
    def _handle_approve_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle approve response (בשמחה - Gladly).
        Send a follow-up message using Twilio API.
        
        Args:
            message: The WhatsApp message with approve button interaction
            
        Returns:
            Response data for approve interaction
        """
        logger.info(f"Handling approve response from {message.profile_name}")
        
        # Use the shared template sending method with approve-specific template
        template_sid = "HXd10781b44eab25e5088956bfa0cfc541"
        return self._send_twilio_template(
            message, 
            template_sid,
            {"response_type": "approve"}
        )
    
    def _handle_not_know_yet_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle "don't know yet" response (לא יודע/ת עדיין).
        Send a follow-up message using Twilio API.
        
        Args:
            message: The WhatsApp message with "don't know yet" button interaction
            
        Returns:
            Response data for "don't know yet" interaction
        """
        logger.info(f"Handling 'don't know yet' response from {message.profile_name}")
        
        # Use the shared template sending method with "don't know yet"-specific template
        template_sid = "HX9eddabf5aea2ec56279755bde2160640"
        return self._send_twilio_template(
            message, 
            template_sid,
            {"response_type": "not_know_yet"}
        )
    
    def _save_to_csv(self, message: WhatsAppMessage, response_value: str) -> None:
        """
        Save message details to CSV file.
        
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
    
    def _handle_numeric_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle numeric responses (1-9).
        Save to CSV and send a follow-up message using Twilio API.
        
        Args:
            message: The WhatsApp message with numeric response
            
        Returns:
            Response data for numeric interaction
        """
        # Extract numeric value
        numeric_value = message.body.strip()
        logger.info(f"Handling numeric response '{numeric_value}' from {message.profile_name}")
        
        # Save to CSV
        self._save_to_csv(message, numeric_value)
        
        # Use the shared template sending method with numeric-specific template
        template_sid = "HXf67e92a3d1ed68775b925abc2dd1d325"
        return self._send_twilio_template(
            message, 
            template_sid,
            {
                "response_type": "numeric", 
                "numeric_value": numeric_value
            }
        )
    
    def _categorize_message(self, message: WhatsAppMessage) -> str:
        """
        Categorize a WhatsApp message.
        
        Simple, focused method with a single responsibility.
        
        Args:
            message: The WhatsApp message
            
        Returns:
            Message type
        """
        # Check for button interactions first
        if message.message_type == 'button':
            logger.info(f"Button interaction detected: {message.button_text} (payload: {message.button_payload})")
            return MessageType.BUTTON
        
        # Use the message body for categorization
        body = message.body.lower()
        
        # Check for numeric response (single digit 1-9)
        if body.strip().isdigit() and len(body.strip()) == 1 and int(body.strip()) in range(1, 10):
            logger.info(f"Numeric response detected: {body}")
            return MessageType.NUMERIC
        
        # Clear, explicit checks for each message type
        if int(message.num_media) > 0:
            return MessageType.MEDIA
            
        if body in ['hi', 'hello', 'שלום', 'היי', 'hey']:
            return MessageType.GREETING
            
        if any(word in body for word in ["rsvp", "אישור", "מגיע", "מגיעים"]):
            return MessageType.RSVP
            
        if '?' in body or any(word in body for word in ["שאלה", "מתי", "איפה", "כמה", "מה"]):
            return MessageType.QUESTION
            
        # Default case
        return MessageType.GENERAL
    
    def handle_status_callback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle status callback data.
        
        Simple method that processes status updates.
        
        Args:
            data: Status callback data
            
        Returns:
            Response data
        """
        # Simple logging - be explicit about what we're doing
        logger.info(f"Processing status callback: {json.dumps(data, indent=2, default=str)}")
        
        # Return simple, consistent response matching test expectations
        return {"status": "status callback processed"}


# Create a default instance for simple imports and backward compatibility
webhook_service = WebhookService()

# Simple function aliases for backward compatibility
def handle_webhook(data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return webhook_service.process_webhook(data)

def handle_whatsapp_message(message: WhatsAppMessage) -> Dict[str, Any]:
    """Function for handling WhatsApp messages."""
    return webhook_service.handle_whatsapp_message(message)

def handle_status_callback(data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return webhook_service.handle_status_callback(data)