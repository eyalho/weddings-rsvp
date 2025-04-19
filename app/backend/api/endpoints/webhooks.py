"""
Webhook endpoints for handling external service callbacks.
"""
from fastapi import APIRouter, Request
import logging
import json
from urllib.parse import unquote_plus

# Services
from backend.services.webhook_service import handle_webhook, handle_status_callback

router = APIRouter()
logger = logging.getLogger(__name__)

def parse_form_data(body_str):
    """Parse URL-encoded form data."""
    form_data = {}
    for param in body_str.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            form_data[key] = unquote_plus(value)
    return form_data

def extract_whatsapp_data(form_data):
    """Extract WhatsApp specific data."""
    # Get basic info
    message = {
        "from": form_data.get("From", "").replace("whatsapp:", ""),
        "to": form_data.get("To", "").replace("whatsapp:", ""),
        "body": form_data.get("Body", ""),
        "profile_name": form_data.get("ProfileName", ""),
        "media_count": form_data.get("NumMedia", "0"),
    }
    
    # Log the message
    logger.info(f"WhatsApp message from {message['profile_name']}: {message['body']}")
    
    return message

# For backward compatibility with tests
def extract_whatsapp_message(form_data):
    """Legacy function to extract WhatsApp message details from form data.
    
    Maintained for backward compatibility with tests.
    """
    message = {
        "message_sid": form_data.get("MessageSid", ""),
        "from_number": form_data.get("From", "").replace("whatsapp:", ""),
        "to_number": form_data.get("To", "").replace("whatsapp:", ""),
        "profile_name": form_data.get("ProfileName", ""),
        "body": form_data.get("Body", ""),
        "num_media": form_data.get("NumMedia", "0"),
        "status": form_data.get("SmsStatus", ""),
        "wa_id": form_data.get("WaId", ""),
    }
    
    # Log the message
    logger.info(f"WhatsApp message from {message['profile_name']}: {message['body']}")
    
    return message

@router.post("/webhook")
async def webhook_endpoint(request: Request):
    """Process incoming webhook requests."""
    logger.info("Webhook request received")
    
    try:
        # Get request body
        body = await request.body()
        body_str = body.decode('utf-8', errors='replace')
        
        # Parse based on content type
        content_type = request.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            # JSON payload
            payload = json.loads(body_str)
            logger.info(f"Received JSON webhook with {len(payload)} keys")
        elif 'application/x-www-form-urlencoded' in content_type:
            # Form data (typical for Twilio)
            form_data = parse_form_data(body_str)
            
            # Check if it's a WhatsApp message
            if 'From' in form_data and 'whatsapp' in form_data.get('From', ''):
                whatsapp_data = extract_whatsapp_data(form_data)
                payload = {
                    "type": "whatsapp",
                    "message": whatsapp_data,
                    "form_data": form_data
                }
            else:
                payload = {
                    "type": "form",
                    "data": form_data
                }
        else:
            # Raw payload
            payload = {"type": "raw", "data": body_str}
            
        # Process the webhook
        return handle_webhook(payload)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

@router.post("/status")
async def status_endpoint(request: Request):
    """Handle status callback requests."""
    logger.info("Status callback received")
    
    try:
        # Get request body
        body = await request.body()
        body_str = body.decode('utf-8', errors='replace')
        
        # Parse based on content type
        content_type = request.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            payload = json.loads(body_str)
        elif 'application/x-www-form-urlencoded' in content_type:
            payload = parse_form_data(body_str)
        else:
            payload = {"raw_data": body_str}
            
        # Process the status callback
        return handle_status_callback(payload)
        
    except Exception as e:
        logger.error(f"Error in status callback: {str(e)}")
        return {"status": "error", "message": str(e)}