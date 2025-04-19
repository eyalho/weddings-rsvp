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
        # Get the raw payload without validation
        body = await request.body()
        log_directly(f"Raw request body: {body}")
        
        payload = await request.json()
        log_directly(f"Received webhook payload: {json.dumps(payload, indent=2)}")
        return handle_webhook(payload)
    except Exception as e:
        error_msg = f"Error in webhook endpoint: {str(e)}"
        log_directly(error_msg)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/status_callback")
async def status_callback_endpoint(request: Request):
    log_directly("Status callback endpoint called")
    
    try:
        # Get the raw payload without validation
        body = await request.body()
        log_directly(f"Raw request body: {body}")
        
        payload = await request.json()
        log_directly(f"Received status callback payload: {json.dumps(payload, indent=2)}")
        return handle_status_callback(payload)
    except Exception as e:
        error_msg = f"Error in status callback endpoint: {str(e)}"
        log_directly(error_msg)
        raise HTTPException(status_code=500, detail=str(e))