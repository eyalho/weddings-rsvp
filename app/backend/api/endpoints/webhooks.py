from fastapi import APIRouter, HTTPException
from ...services.webhook_service import handle_webhook, handle_status_callback

router = APIRouter()

@router.post("/webhook")
async def webhook_endpoint(payload: dict):
    try:
        return handle_webhook(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/status_callback")
async def status_callback_endpoint(payload: dict):
    try:
        return handle_status_callback(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))