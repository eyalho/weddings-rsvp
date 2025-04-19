"""
Frontend routes module.

Handles frontend route setup following:
- "Simple is better than complex"
- "Explicit is better than implicit"
"""
import os
import logging
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from .config import Settings, get_settings
from .exceptions import NotFoundError

# Simple, module-level logger
logger = logging.getLogger(__name__)

def setup_frontend_routes(app: FastAPI, settings: Optional[Settings] = None) -> None:
    """
    Set up routes for serving the frontend application.
    
    Simple, explicit function that handles frontend route setup
    with clear error handling.
    
    Args:
        app: FastAPI application
        settings: Optional Settings, obtained from get_settings() if None
    """
    # Get settings if not provided
    if settings is None:
        settings = get_settings()
    
    # Frontend path from settings
    frontend_path = settings.FRONTEND_PATH
    
    # Explicitly check and handle missing frontend
    if not os.path.exists(frontend_path):
        logger.warning(f"Frontend build not found at: {frontend_path}")
        
        # Add simple API root when frontend is missing
        @app.get("/", include_in_schema=False)
        async def api_root():
            """Simple API root endpoint when no frontend is available."""
            logger.info("Serving API welcome message (no frontend)")
            return JSONResponse({
                "message": f"Welcome to {settings.PROJECT_NAME}",
                "status": "api_only_mode",
                "docs_url": "/docs" if settings.DEBUG else None
            })
        return
    
    # Log setup - make it clear what's happening
    logger.info(f"Setting up frontend routes from: {frontend_path}")
    
    # Mount static files - explicit check for directory existence
    static_dir = os.path.join(frontend_path, "static")
    if os.path.exists(static_dir):
        app.mount(
            "/static", 
            StaticFiles(directory=static_dir), 
            name="static"
        )
        logger.info(f"Static files mounted from: {static_dir}")
    else:
        logger.warning(f"Static directory not found at: {static_dir}")
    
    # Add root route to serve index.html
    @app.get("/", include_in_schema=False)
    async def frontend_root():
        """Serve the frontend index.html for the root URL."""
        index_path = os.path.join(frontend_path, "index.html")
        logger.info(f"Serving frontend index from: {index_path}")
        return FileResponse(index_path)
    
    # Add catch-all route for SPA navigation with very low priority (must be registered last)
    @app.get("/{catch_all:path}", include_in_schema=False)
    async def frontend_catchall(catch_all: str, request: Request):
        """
        Serve the frontend for all non-API routes.
        
        This handler should only be called after all other routes (including API routes) have been checked.
        
        Args:
            catch_all: The path being requested
            request: The request object
            
        Returns:
            Frontend index.html for frontend routes
        """
        # Get the full path from the request
        full_path = request.url.path
        
        # Bypass this handler for API routes
        # API routes should be handled by their own handlers, so if we get here with an API path,
        # it means the route doesn't exist (already a 404)
        if full_path.startswith(settings.API_V1_STR):
            logger.warning(f"API route not found: {full_path}")
            # Pass to the next handler or let FastAPI generate a 404
            # DO NOT raise an exception here - let FastAPI handle it
            raise NotFoundError(f"API route not found: {full_path}")
            
        # For non-API routes, serve the frontend
        logger.info(f"Serving frontend for path: {catch_all}")
        return FileResponse(os.path.join(frontend_path, "index.html")) 