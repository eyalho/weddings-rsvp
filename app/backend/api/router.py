"""
API router module.

Central router for all API endpoints following:
- "Explicit is better than implicit"
- "Simple is better than complex"
"""
from fastapi import APIRouter, Depends

from app.backend.core.dependencies import get_settings
from app.backend.api.endpoints.webhooks import router as webhooks_router

# Create the main API router - a simple, focused component
api_router = APIRouter()

# Explicitly register all endpoint routers
api_router.include_router(
    webhooks_router,
    prefix="/webhooks",  # make the URL path more RESTful
    tags=["webhooks"]    # explicit OpenAPI tag
)

# Additional routers can be added here following the same pattern
# api_router.include_router(
#     some_router,
#     prefix="/path",
#     tags=["tag"]
# ) 