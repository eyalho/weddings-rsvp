from fastapi import APIRouter, HTTPException, Request, Form
from ...services.webhook_service import handle_webhook, handle_status_callback
import logging
import sys
import json
from urllib.parse import parse_qs

router = APIRouter()
logger = logging.getLogger(__name__)

# Direct print function that ensures output is visible
def log_directly(message):
    print(f"WEBHOOK_DEBUG: {message}", flush=True)
    sys.stdout.write(f"WEBHOOK_DIRECT_LOG: {message}\n")
    sys.stdout.flush()
    logger.warning(message)

@router.post("/webhook")
async def webhook_endpoint(request: Request):
    log_directly("Webhook endpoint called")
    
    try:
        # Get the raw request details
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        log_directly(f"Request details: Method={method}, URL={url}")
        log_directly(f"Content-Type: {headers.get('content-type', 'Not specified')}")
        
        # Read the raw body
        body = await request.body()
        body_str = body.decode('utf-8', errors='replace')
        log_directly(f"Raw request body ({len(body_str)} chars): '{body_str}'")
        
        # If body is empty, handle gracefully
        if not body_str or body_str.isspace():
            log_directly("Empty request body received")
            return {"status": "webhook processed", "message": "Empty request received"}
        
        # Check content type and parse accordingly
        content_type = headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            # Handle JSON data
            try:
                payload = json.loads(body_str)
                log_directly(f"Parsed JSON payload: {json.dumps(payload, indent=2)}")
            except json.JSONDecodeError as je:
                log_directly(f"JSON parsing failed: {str(je)}")
                return {"status": "error", "message": f"Invalid JSON: {str(je)}"}
        
        elif 'application/x-www-form-urlencoded' in content_type or '&' in body_str and '=' in body_str:
            # Handle form data (typical for Twilio webhooks)
            try:
                # Parse form data
                form_data = {}
                params = body_str.split('&')
                for param in params:
                    if '=' in param:
                        key, value = param.split('=', 1)
                        form_data[key] = value
                
                log_directly(f"Parsed form data: {json.dumps(form_data, indent=2)}")
                payload = form_data
                
                # Check if this is a Twilio WhatsApp message
                if 'From' in form_data and 'whatsapp' in form_data.get('From', ''):
                    log_directly("Detected Twilio WhatsApp webhook")
                    # Extract the key message details
                    from_number = form_data.get('From', '').replace('whatsapp:', '')
                    message_body = form_data.get('Body', '')
                    log_directly(f"WhatsApp message from {from_number}: {message_body}")
            except Exception as e:
                log_directly(f"Form data parsing failed: {str(e)}")
                # Create a simple payload from the raw body
                payload = {"raw_data": body_str}
        else:
            # Handle as raw data
            log_directly("Unknown content type, treating as raw data")
            payload = {"raw_data": body_str}
        
        # Process the webhook with the parsed payload
        return handle_webhook(payload)
            
    except Exception as e:
        error_msg = f"Error in webhook endpoint: {str(e)}"
        log_directly(error_msg)
        return {"status": "error", "message": str(e)}

@router.post("/status_callback")
async def status_callback_endpoint(request: Request):
    log_directly("Status callback endpoint called")
    
    try:
        # Get the raw request details
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        log_directly(f"Request details: Method={method}, URL={url}")
        log_directly(f"Headers: {json.dumps(headers, indent=2)}")
        
        # Read the raw body
        body = await request.body()
        body_str = body.decode('utf-8', errors='replace')
        log_directly(f"Raw request body ({len(body_str)} chars): '{body_str}'")
        
        # If body is empty, handle gracefully
        if not body_str or body_str.isspace():
            log_directly("Empty request body received")
            return {"status": "status callback processed", "message": "Empty request received"}
        
        # Try to parse as JSON
        try:
            payload = json.loads(body_str)
            log_directly(f"Parsed JSON payload: {json.dumps(payload, indent=2)}")
            return handle_status_callback(payload)
        except json.JSONDecodeError as je:
            log_directly(f"JSON parsing failed: {str(je)}")
            # Try to parse as form data
            try:
                form_data = {}
                params = body_str.split('&')
                for param in params:
                    if '=' in param:
                        key, value = param.split('=', 1)
                        form_data[key] = value
                
                log_directly(f"Parsed form data: {json.dumps(form_data, indent=2)}")
                return handle_status_callback(form_data)
            except Exception as e:
                log_directly(f"Form data parsing failed: {str(e)}")
                return {"status": "error", "message": "Could not parse request data"}
            
    except Exception as e:
        error_msg = f"Error in status callback endpoint: {str(e)}"
        log_directly(error_msg)
        return {"status": "error", "message": str(e)}