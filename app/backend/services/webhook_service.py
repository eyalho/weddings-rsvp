"""
Webhook service module.

Handles webhook data processing following:
- "Simple is better than complex"
- "Explicit is better than implicit"
- "Readability counts"
"""
import json
import logging
from typing import Dict, Any, Optional, List, Union
from enum import Enum
from dataclasses import dataclass

# Import from separated service modules
from backend.services.storage import DataStorage
from backend.services.twilio_service import TwilioMessageSender

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """
    Explicit message type enumeration.
    
    Makes valid message types explicit rather than using magic strings.
    """
    GREETING = "greeting"
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
    https://www.twilio.com/docs/messaging/guides/webhook-request
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


class MessageCategorizer:
    """
    Service for categorizing messages.
    
    Classifies messages into appropriate message types.
    """
    
    def categorize(self, message: WhatsAppMessage) -> str:
        """
        Categorize a WhatsApp message.
        
        Args:
            message: The WhatsApp message
            
        Returns:
            Message type
        """
        # Check for button interactions first
        if message.button_text or message.button_payload:
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
            
        if '?' in body or any(word in body for word in ["שאלה", "מתי", "איפה", "כמה", "מה"]):
            return MessageType.QUESTION
            
        # Default case
        return MessageType.GENERAL


class ResponseHandler:
    """
    Service for handling different types of responses.
    
    Provides specialized handling for different message and response types.
    """
    
    def __init__(self):
        self.twilio_sender = TwilioMessageSender()
        self.data_storage = DataStorage()
    
    def handle_decline_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle decline response (לצערי לא - Unfortunately not).
        
        Args:
            message: The WhatsApp message with decline button interaction
            
        Returns:
            Response data for decline interaction
        """
        logger.info(f"Handling decline response from {message.profile_name}")
        
        # Use the shared template sending method with decline-specific template
        template_sid = "HX4b154aac4a81de7cebb4cb42fbd837a9"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {"response_type": "decline"}
        )
    
    def handle_approve_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle approve response (כן, אגיע! - Yes, I'll come!).
        
        Args:
            message: The WhatsApp message with approve button interaction
            
        Returns:
            Response data for approve interaction
        """
        logger.info(f"Handling approve response from {message.profile_name}")
        
        # Use the shared template sending method with approve-specific template
        template_sid = "HXd10781b44eab25e5088956bfa0cfc541"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {"response_type": "approve"}
        )
    
    def handle_not_know_yet_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle "don't know yet" response (עוד לא יודע/ת - Don't know yet).
        
        Args:
            message: The WhatsApp message with "don't know yet" button interaction
            
        Returns:
            Response data for "don't know yet" interaction
        """
        logger.info(f"Handling 'don't know yet' response from {message.profile_name}")
        
        # Use the shared template sending method with "don't know yet"-specific template
        template_sid = "HX9eddabf5aea2ec56279755bde2160640"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {"response_type": "not_know_yet"}
        )
    
    def handle_numeric_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle numeric responses (1-9).
        
        Args:
            message: The WhatsApp message with numeric response
            
        Returns:
            Response data for numeric interaction
        """
        # Extract numeric value
        numeric_value = message.body.strip()
        logger.info(f"Handling numeric response '{numeric_value}' from {message.profile_name}")
        
        # Save to CSV
        self.data_storage.save_numeric_response(message, numeric_value)
        
        # Use the shared template sending method with numeric-specific template
        template_sid = "HXf67e92a3d1ed68775b925abc2dd1d325"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {
                "response_type": "numeric", 
                "numeric_value": numeric_value
            }
        )
    
    def handle_button_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
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
            return self.handle_decline_response(message)
        elif message.button_text == "כן, אגיע!" and message.button_payload == "1":
            # Custom response for approval button
            return self.handle_approve_response(message)
        elif message.button_text == "עוד לא יודע/ת" and message.button_payload == "3":
            # Custom response for "Don't know yet" button 
            return self.handle_not_know_yet_response(message)
            
        # Default button response
        return {
            "status": "button_response_processed",
            "message_type": MessageType.BUTTON,
            "button_text": message.button_text,
            "button_payload": message.button_payload,
            "from": message.from_number
        }


class WebhookService:
    """
    Main service for processing webhook data.
    
    Orchestrates the processing of webhook requests by delegating to specialized services.
    """
    
    def __init__(self):
        self.message_categorizer = MessageCategorizer()
        self.response_handler = ResponseHandler()
    
    def process_webhook(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook data.
        
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
        
        Args:
            message: The WhatsApp message data as a WhatsAppMessage object
        Returns:
            Response data with message type
        """
        # Log what we're processing
        logger.info(f"Processing WhatsApp message from {message.profile_name}")
        
        # Determine message type - explicit categorization
        message_type = self.message_categorizer.categorize(message)
        
        # Log the categorization
        logger.info(
            f"Message from {message.from_number} categorized as {message_type}"
        )
        
        # Handle different message types
        if message_type == MessageType.BUTTON:
            return self.response_handler.handle_button_response(message)
        elif message_type == MessageType.NUMERIC:
            return self.response_handler.handle_numeric_response(message)
        
        # Return a simple, consistent response matching test expectations
        return {
            "status": "whatsapp_message_processed",
            "message_type": message_type,
            "from": message.from_number
        }
    
    def handle_status_callback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle status callback data.
        
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