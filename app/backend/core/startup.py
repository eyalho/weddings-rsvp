"""
Application startup module.
Handles startup tasks and initialization.
"""
import logging
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from .config import settings
from .logging_config import setup_logging
from .exceptions import AppException, app_exception_handler, validation_exception_handler, generic_exception_handler
from .middleware import RequestLoggingMiddleware
from .routes import setup_frontend_routes

logger = logging.getLogger(__name__)

def startup_event(app: FastAPI) -> None:
    """Run startup tasks for the application.
    
    This function is called when the application starts up.
    
    Args:
        app: FastAPI application instance
    """
    logger.info("Running application startup tasks")
    
    # Additional startup tasks can be added here
    # For example:
    # - Database connections
    # - Cache initialization
    # - External service health checks
    
    logger.info("Application startup complete")

def shutdown_event(app: FastAPI) -> None:
    """Run shutdown tasks for the application.
    
    This function is called when the application shuts down.
    
    Args:
        app: FastAPI application instance
    """
    logger.info("Running application shutdown tasks")
    
    # Additional shutdown tasks can be added here
    # For example:
    # - Close database connections
    # - Clear caches
    # - Release resources
    
    logger.info("Application shutdown complete")

def init_app() -> FastAPI:
    """Initialize the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    # Set up logging first
    setup_logging(log_to_stdout=True)
    
    # Create FastAPI app with initial configuration
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for Wedding RSVP and guest management",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        debug=settings.DEBUG,
    )
    
    # Register startup and shutdown event handlers
    app.add_event_handler("startup", lambda: startup_event(app))
    app.add_event_handler("shutdown", lambda: shutdown_event(app))
    
    # Register exception handlers
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add custom middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Setup routes for the frontend
    setup_frontend_routes(app)
    
    # Ensure all parent directories are in the path for imports
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    # Setup API routes with relative import
    from ..api.endpoints import router as api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    logger.info(f"Application initialized: {settings.PROJECT_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    return app 