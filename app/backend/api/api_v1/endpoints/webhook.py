"""
WhatsApp webhook endpoints.

This module handles WhatsApp webhook requests including incoming messages and status callbacks.
"""
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.backend.core.config import get_settings
from app.backend.db.session import get_db
from app.backend.db import crud
from app.backend.services.webhook_service import WebhookService, WhatsAppMessage
from app.backend.services.conversation_service import ConversationService

router = APIRouter()
settings = get_settings()
webhook_service = WebhookService()


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Handle incoming WhatsApp webhook requests.
    
    This endpoint processes incoming messages from WhatsApp, parses them,
    categorizes the message type, and hands them off to the conversation service
    to generate appropriate responses.
    """
    try:
        data = await request.form()
        message = webhook_service.process_webhook(dict(data))
        
        # Initialize conversation service with the database session
        conversation_service = ConversationService(db)
        
        # Process the message and get a response
        response = conversation_service.process_message(message)
        
        return {"success": True, "message": "Webhook processed successfully", "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )


@router.post("/status")
async def status_callback(
    request: Request,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    Handle message status callback from Twilio.
    
    This endpoint processes status updates for messages sent via Twilio,
    which allows tracking when messages are delivered, read, etc.
    """
    try:
        data = await request.form()
        webhook_service.handle_status_callback(dict(data))
        
        # Store status information in the database if needed
        # This could be used for analytics or debugging
        
        return {"success": True, "message": "Status callback processed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process status callback: {str(e)}"
        )


@router.get("/verify")
async def verify_webhook(request: Request) -> Dict[str, Any]:
    """
    Verify webhook endpoint for WhatsApp Business API setup.
    
    WhatsApp/Meta requires verification of webhook endpoints during setup.
    This endpoint responds to verification requests with the appropriate challenge.
    """
    params = dict(request.query_params)
    
    # Check for hub.mode and hub.verify_token parameters
    mode = params.get('hub.mode')
    token = params.get('hub.verify_token')
    challenge = params.get('hub.challenge')
    
    # Verify that the mode and token are valid
    if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
        if challenge:
            return {"hub.challenge": challenge}
        return {"success": True, "message": "Webhook verified successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Verification failed"
    ) 