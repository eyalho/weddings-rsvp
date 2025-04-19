"""
Central API router for all backend endpoints.
"""
from fastapi import APIRouter

# Import webhook router and RSVP router
from backend.api.endpoints.webhook import router as webhook_router
from backend.api.endpoints.rsvp import router as rsvp_router

# Create main API router
api_router = APIRouter()

# Register the webhook router
api_router.include_router(webhook_router, tags=["webhook"])

# Register the RSVP router
api_router.include_router(rsvp_router, prefix="/rsvp", tags=["rsvp"]) 