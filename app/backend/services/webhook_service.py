import logging
import json
import sys
from pprint import pformat

# Don't configure logging here, use the configuration from main.py
# logging.basicConfig() calls should only happen once in the application
logger = logging.getLogger(__name__)

def handle_webhook(data: dict):
    """Process incoming webhook data.
    
    This function handles different types of webhook data,
    with special handling for WhatsApp messages.
    """
    logger.warning(f"Processing webhook data of type: {data.get('message_type', 'unknown')}")
    
    # Check if this is a WhatsApp message
    if data.get('message_type') == 'whatsapp':
        return handle_whatsapp_message(data['whatsapp_message'])
    
    # Add verbose debugging output (using warning level to ensure it's printed)
    logger.warning("Webhook payload details:")
    logger.warning("=" * 50)
    logger.warning("Content type: %s", type(data))
    logger.warning("Content structure:\n%s", pformat(data, indent=2))
    
    try:
        # Pretty print the JSON for better readability in logs
        pretty_json = json.dumps(data, indent=2, sort_keys=True)
        logger.warning("Full webhook content:\n%s", pretty_json)
    except Exception as e:
        logger.error("Error printing webhook content: %s", str(e))
    
    logger.warning("=" * 50)
    
    return {"status": "webhook processed"}

def handle_whatsapp_message(message: dict):
    """Handle a WhatsApp message from Twilio.
    
    This function processes the structured WhatsApp message data
    and takes appropriate actions based on the message content.
    """
    logger.warning(f"Processing WhatsApp message from {message['profile_name']}")
    
    # Extract key information
    from_number = message['from_number']
    message_body = message['body']
    
    # Example: Respond differently based on message content
    response = {"status": "whatsapp_message_processed"}
    
    # You could implement different actions based on message content
    if message_body.lower() in ['hi', 'hello', 'שלום']:
        logger.warning(f"Greeting received from {from_number}")
        response["message_type"] = "greeting"
    elif "rsvp" in message_body.lower() or "אישור" in message_body:
        logger.warning(f"RSVP intent detected from {from_number}")
        response["message_type"] = "rsvp"
    elif "?" in message_body or "שאלה" in message_body:
        logger.warning(f"Question detected from {from_number}")
        response["message_type"] = "question"
    else:
        logger.warning(f"General message from {from_number}")
        response["message_type"] = "general"
    
    # You would typically store this message in your database here
    # db.save_message(message)
    
    return response

def handle_status_callback(data: dict):
    # Logic to process status updates
    logger.warning("Processing status callback data: %s", data)
    return {"status": "status callback processed"}