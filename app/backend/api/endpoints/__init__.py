"""
API endpoints package.
Contains all API routers and endpoint definitions.
"""
from fastapi import APIRouter
from backend.api.endpoints.webhooks import router as webhooks_router

# Create a main API router
router = APIRouter()

# Include all endpoint routers
router.include_router(webhooks_router, tags=["webhooks"]) 