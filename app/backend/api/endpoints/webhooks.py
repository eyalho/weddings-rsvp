from fastapi import APIRouter, HTTPException, Request
from ...services.webhook_service import handle_webhook, handle_status_callback
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def webhook_endpoint(request: Request):
    logger.warning("Webhook endpoint called")
    
    try:
        # Get the raw payload without validation
        payload = await request.json()
        logger.warning(f"Received webhook payload: {payload}")
        return handle_webhook(payload)
    except Exception as e:
        logger.error(f"Error in webhook endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/status_callback")
async def status_callback_endpoint(request: Request):
    logger.warning("Status callback endpoint called")
    
    try:
        # Get the raw payload without validation
        payload = await request.json()
        logger.warning(f"Received status callback payload: {payload}")
        return handle_status_callback(payload)
    except Exception as e:
        logger.error(f"Error in status callback endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))