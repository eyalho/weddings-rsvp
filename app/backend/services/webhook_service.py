"""
Webhook service module.

Handles webhook data processing following:
- "Simple is better than complex"
- "Explicit is better than implicit"
- "Readability counts"
"""
import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

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
        logger.info(f"Processing webhook data type: {data.get('type', 'unknown')}")
        
        # Check if this is a WhatsApp message
        if data.get('type') == 'whatsapp' and 'message' in data:
            whatsapp_data = data['message']
            # Check form data for direct message handling
            form_data = data.get('form_data', {})
            
            # Use the extract_whatsapp_message format for backward compatibility with tests
            whatsapp_message = {
                "message_sid": form_data.get("MessageSid", ""),
                "from_number": whatsapp_data.get("from", ""),
                "to_number": whatsapp_data.get("to", ""),
                "profile_name": whatsapp_data.get("profile_name", ""),
                "body": whatsapp_data.get("body", ""),
                "num_media": whatsapp_data.get("media_count", "0"),
                "status": form_data.get("SmsStatus", ""),
                "wa_id": form_data.get("WaId", ""),
            }
            
            return self.handle_whatsapp_message(whatsapp_message)
        
        # Handle empty data
        if not data or (isinstance(data, dict) and len(data) == 0) or (isinstance(data, str) and not data.strip()):
            return {"status": "webhook processed", "message": "Empty request", "type": "empty"}
            
        # Simple logging of payload details
        logger.info(f"Generic webhook payload: {json.dumps(data, indent=2, default=str)}")
        
        # Simple, consistent response matching test expectations
        return {"status": "webhook processed", "type": "generic"}
    
    def handle_whatsapp_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a WhatsApp message.
        
        Simple method that categorizes messages and returns appropriate responses.
        
        Args:
            message: The WhatsApp message data
            
        Returns:
            Response data with message type
        """
        # Create structured message object - makes code more readable
        whatsapp_msg = WhatsAppMessage(
            message_sid=message.get('message_sid', ''),
            from_number=message.get('from_number', ''),
            to_number=message.get('to_number', ''),
            profile_name=message.get('profile_name', ''),
            body=message.get('body', ''),
            num_media=message.get('num_media', '0'),
            status=message.get('status', ''),
            wa_id=message.get('wa_id', ''),
            media=message.get('media', [])
        )
        
        # Log what we're processing
        logger.info(f"Processing WhatsApp message from {whatsapp_msg.profile_name}")
        
        # Determine message type - explicit categorization
        message_type = self.categorize_message(whatsapp_msg)
        
        # Log the categorization
        logger.info(
            f"Message from {whatsapp_msg.from_number} categorized as {message_type}"
        )
        
        # Here you would typically store the message in a database
        # self.save_message(whatsapp_msg, message_type)
        
        # Return a simple, consistent response matching test expectations
        return {
            "status": "whatsapp_message_processed",
            "message_type": message_type,
            "from": whatsapp_msg.from_number
        }
    
    def categorize_message(self, message: WhatsAppMessage) -> str:
        """
        Categorize a WhatsApp message.
        
        Simple, focused method with a single responsibility.
        
        Args:
            message: The WhatsApp message
            
        Returns:
            Message type
        """
        # Use the message body for categorization
        body = message.body.lower()
        
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

def handle_whatsapp_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return webhook_service.handle_whatsapp_message(message)

def handle_status_callback(data: Dict[str, Any]) -> Dict[str, Any]:
    """Legacy function for backward compatibility."""
    return webhook_service.handle_status_callback(data)