"""
Twilio service module.

Handles interactions with the Twilio API for sending WhatsApp messages.
"""
import json
import logging
import os
import re
from typing import Dict, Any

# Module-level logger with explicit name
logger = logging.getLogger(__name__)


class TwilioMessageSender:
    """
    Service for sending messages via Twilio.
    
    Handles all Twilio API interactions.
    """
    
    def send_template(self, message, template_sid: str, additional_data: Dict = None) -> Dict[str, Any]:
        """
        Send a message using Twilio template.
        
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
            "message_type": "button", # Using string instead of MessageType to avoid circular import
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