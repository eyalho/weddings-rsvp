"""
Webhook endpoints for handling external service callbacks.
"""
from fastapi import APIRouter, Request
import logging
import json
from urllib.parse import unquote_plus

# Services
from backend.services.webhook_service import (
    handle_webhook, 
    handle_status_callback, 
    handle_whatsapp_message,
    WhatsAppMessage
)

router = APIRouter()
logger = logging.getLogger(__name__)

def parse_form_data(body_str):
    """Parse URL-encoded form data."""
    form_data = {}
    logger.info(f"Parsing form data: {body_str}")
    for param in body_str.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            form_data[key] = unquote_plus(value)
    logger.info(f"Parsed form data: {form_data}")
    return form_data

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
        
        # Handle JSON payloads
        if 'application/json' in content_type:
            # JSON payload
            json_data = json.loads(body_str)
            logger.info(f"Received JSON webhook with {len(json_data)} keys")
            
            # Check if this is a WhatsApp message in JSON format
            if json_data.get('type') == 'whatsapp' and 'message' in json_data:
                message_data = json_data['message']
                form_data = json_data.get('form_data', {})
                
                # Create WhatsAppMessage directly
                whatsapp_message = WhatsAppMessage(
                    message_sid=form_data.get("MessageSid", ""),
                    from_number=message_data.get("from", ""),
                    to_number=message_data.get("to", ""),
                    profile_name=message_data.get("profile_name", ""),
                    body=message_data.get("body", ""),
                    num_media=message_data.get("media_count", "0"),
                    status=form_data.get("SmsStatus", ""),
                    wa_id=form_data.get("WaId", ""),
                    message_type=message_data.get("MessageType", ""),
                    button_text=message_data.get("ButtonText", ""),
                    button_payload=message_data.get("ButtonPayload", ""),
                    original_replied_message_sid=message_data.get("OriginalRepliedMessageSid", ""),
                    original_replied_message_sender=message_data.get("OriginalRepliedMessageSender", "")
                )
                logger.info(f"WhatsApp message from {whatsapp_message.profile_name}: {whatsapp_message.body}")
                
                # Process WhatsApp message directly
                return handle_whatsapp_message(whatsapp_message)
            
            # Handle other JSON payloads
            return handle_webhook(json_data)

        # Handle form data (typical for Twilio)
        elif 'application/x-www-form-urlencoded' in content_type:
            form_data = parse_form_data(body_str)
            
            # Check if it's a WhatsApp message
            if 'From' in form_data and 'whatsapp' in form_data.get('From', ''):
                # Create WhatsAppMessage directly
                whatsapp_message = WhatsAppMessage(
                    message_sid=form_data.get("MessageSid", ""),
                    from_number=form_data.get("From", "").replace("whatsapp:", ""),
                    to_number=form_data.get("To", "").replace("whatsapp:", ""),
                    profile_name=form_data.get("ProfileName", ""),
                    body=form_data.get("Body", ""),
                    num_media=form_data.get("NumMedia", "0"),
                    status=form_data.get("SmsStatus", ""),
                    wa_id=form_data.get("WaId", ""),
                    button_text=form_data.get("ButtonText", ""),
                    button_payload=form_data.get("ButtonPayload", ""),
                    original_replied_message_sid=form_data.get("OriginalRepliedMessageSid", ""),
                    original_replied_message_sender=form_data.get("OriginalRepliedMessageSender", "")
                )
                logger.info(f"WhatsApp message from {whatsapp_message.profile_name}: {whatsapp_message.body} {whatsapp_message}")
                
                # Process WhatsApp message directly
                return handle_whatsapp_message(whatsapp_message)
            
            # Handle other form data
            return handle_webhook({
                "type": "form",
                "data": form_data
            })
        
        # Handle other content types
        else:
            # Raw payload
            return handle_webhook({
                "type": "raw", 
                "data": body_str
            })
        
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