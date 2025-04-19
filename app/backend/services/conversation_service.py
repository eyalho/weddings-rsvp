"""
Conversation service module.

Handles conversation flow and persistence using SQLAlchemy models.
"""
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from app.backend.db import crud
from app.backend.services.webhook_service import WhatsAppMessage, MessageType
from app.backend.services.twilio_service import TwilioMessageSender

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class ConversationService:
    """
    Service for managing conversations and interactions.
    
    This class handles the persistence and retrieval of conversation data
    using SQLAlchemy models, and provides methods for responding to
    different types of messages.
    """
    
    def __init__(self, db: Session):
        """
        Initialize the conversation service with a database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.twilio_sender = TwilioMessageSender()
    
    def process_message(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Process an incoming WhatsApp message.
        
        This method determines the appropriate response based on message type,
        saves the message to the database, and returns a response.
        
        Args:
            message: The WhatsApp message to process
            
        Returns:
            Response data for the message
        """
        logger.info(f"Processing message from {message.profile_name} ({message.from_number})")
        
        # Determine message type
        message_type = self._categorize_message(message)
        
        # Save message to database - use the appropriate question key
        question_key = "general_message"
        if message_type == MessageType.BUTTON:
            question_key = "button_response"
        elif message_type == MessageType.NUMERIC:
            question_key = "numeric_response"
        elif message_type == MessageType.GREETING:
            question_key = "greeting"
        elif message_type == MessageType.QUESTION:
            question_key = "question"
        
        # Create user response record using SQLAlchemy model
        response_data = {
            "phone_number": message.from_number,
            "question_key": question_key,
            "response_text": message.body,
            "response_value": message.button_payload if message_type == MessageType.BUTTON else (
                message.body.strip() if message_type == MessageType.NUMERIC else ""
            )
        }
        
        # Save to database using CRUD operations
        user_response = crud.create_user_response(self.db, response_data)
        
        # Process message based on type
        if message_type == MessageType.BUTTON:
            return self._handle_button_response(message)
        elif message_type == MessageType.NUMERIC:
            return self._handle_numeric_response(message)
        elif message_type == MessageType.GREETING:
            return self._handle_greeting(message)
        elif message_type == MessageType.QUESTION:
            return self._handle_question(message)
        else:
            return self._handle_general_message(message)
    
    def _categorize_message(self, message: WhatsAppMessage) -> str:
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
    
    def _handle_decline_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
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
    
    def _handle_approve_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
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
    
    def _handle_not_know_yet_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
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
    
    def _handle_numeric_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
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
    
    def _handle_greeting(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle greeting messages.
        
        Args:
            message: The WhatsApp message with greeting
            
        Returns:
            Response data for greeting
        """
        logger.info(f"Handling greeting from {message.profile_name}")
        
        # Use a template for greeting responses
        template_sid = "HX9f1d4a8bc3a25db4a6b6a8e66f72f7dc"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {"response_type": "greeting"}
        )
    
    def _handle_question(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle question messages.
        
        Args:
            message: The WhatsApp message with question
            
        Returns:
            Response data for question
        """
        logger.info(f"Handling question from {message.profile_name}: {message.body}")
        
        # Use a template for question responses
        template_sid = "HX75d9b6aa1adce7d6b8bc88f7e1c95d5d"
        return self.twilio_sender.send_template(
            message, 
            template_sid,
            {"response_type": "question"}
        )
    
    def _handle_general_message(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """
        Handle general messages.
        
        Args:
            message: The WhatsApp message
            
        Returns:
            Response data for general message
        """
        logger.info(f"Handling general message from {message.profile_name}: {message.body}")
        
        # Default response for general messages
        return {
            "status": "general_message_processed",
            "message_type": MessageType.GENERAL,
            "from": message.from_number
        } 