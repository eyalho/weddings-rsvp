"""
API V1 router.

This module includes all API routes for version 1 of the API.
"""
from fastapi import APIRouter

from app.backend.api.api_v1.endpoints import webhook, rsvp

api_router = APIRouter()
api_router.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
api_router.include_router(rsvp.router, prefix="/rsvp", tags=["rsvp"]) 