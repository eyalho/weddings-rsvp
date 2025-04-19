from fastapi import APIRouter, HTTPException, Request
from ...services.webhook_service import handle_webhook, handle_status_callback
import logging
import sys
import json

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
        log_directly(f"Headers: {json.dumps(headers, indent=2)}")
        
        # Read the raw body
        body = await request.body()
        body_str = body.decode('utf-8', errors='replace')
        log_directly(f"Raw request body ({len(body_str)} chars): '{body_str}'")
        
        # If body is empty, handle gracefully
        if not body_str or body_str.isspace():
            log_directly("Empty request body received")
            return {"status": "webhook processed", "message": "Empty request received"}
        
        # Try to parse as JSON
        try:
            payload = json.loads(body_str)
            log_directly(f"Parsed JSON payload: {json.dumps(payload, indent=2)}")
            return handle_webhook(payload)
        except json.JSONDecodeError as je:
            log_directly(f"JSON parsing failed: {str(je)}")
            return {"status": "error", "message": f"Invalid JSON: {str(je)}"}
            
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
            return {"status": "error", "message": f"Invalid JSON: {str(je)}"}
            
    except Exception as e:
        error_msg = f"Error in status callback endpoint: {str(e)}"
        log_directly(error_msg)
        return {"status": "error", "message": str(e)}