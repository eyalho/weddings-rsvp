"""
API endpoints package.
Contains all API routers and endpoint definitions.
"""
from fastapi import APIRouter
from backend.api.endpoints.webhook import router as webhook_router

# Create a main API router
router = APIRouter()

# Include all endpoint routers
router.include_router(webhook_router, tags=["webhook"]) 