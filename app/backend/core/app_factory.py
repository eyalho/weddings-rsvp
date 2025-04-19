"""
Application factory module for the backend API.
"""
import logging
import sys
import os
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .logging_config import configure_logging
from .exception_handlers import register_exception_handlers
from .middleware import add_middlewares
from .routes import setup_frontend_routes

logger = logging.getLogger(__name__)

def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    # Get settings
    if settings is None:
        settings = get_settings()
    
    # Configure logging
    configure_logging(level=settings.LOG_LEVEL)
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for Wedding RSVP and guest management",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        debug=settings.DEBUG,
    )
    
    # Register startup/shutdown events
    @app.on_event("startup")
    async def startup_event():
        logger.info("Application startup")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Application shutdown")
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware
    add_middlewares(app, settings)
    
    # Setup frontend routes
    setup_frontend_routes(app)
    
    # Setup path for relative imports
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    # Import and register API router
    try:
        # Try relative import first
        from ..api.router import api_router
    except ImportError:
        # Fall back to absolute import if needed
        from api.router import api_router
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Log routes on startup for debugging
    @app.on_event("startup")
    async def log_routes():
        routes = [f"{route.path}" for route in app.routes]
        logger.info(f"Registered routes: {len(routes)} routes")
        for route in sorted(routes):
            logger.info(f"Route: {route}")
    
    logger.info(f"Application initialized: {settings.PROJECT_NAME}")
    
    return app 