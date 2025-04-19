"""
Central API router for all backend endpoints.
"""
from fastapi import APIRouter, Request
import logging
import json

from .endpoints.webhooks import router as webhooks_router

# Create main API router
api_router = APIRouter()

# Register the webhooks router
api_router.include_router(webhooks_router)

# Direct webhook endpoints at the API root level
@api_router.get("/webhook")
async def webhook_get():
    """Test endpoint for webhook verification."""
    return {"status": "success", "message": "Webhook endpoint is active"}

@api_router.post("/webhook")
async def webhook_post(request: Request):
    """Main webhook endpoint for processing incoming requests."""
    try:
        body = await request.body()
        body_text = body.decode("utf-8", errors="replace")
        
        # Process form data
        if request.headers.get("content-type") == "application/x-www-form-urlencoded":
            form_data = {}
            for param in body_text.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    form_data[key] = value
            return {"status": "success", "message": "Webhook received", "type": "form"}
        
        # Process JSON data
        try:
            json_data = json.loads(body_text)
            return {"status": "success", "message": "Webhook received", "type": "json"}
        except:
            pass
            
        # Default response
        return {"status": "success", "message": "Webhook received", "type": "raw"}
    except Exception as e:
        return {"status": "error", "message": str(e)} 