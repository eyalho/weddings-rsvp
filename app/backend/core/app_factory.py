"""
Application factory module.

Provides a simple, explicit function to create and configure the FastAPI application.
Follows the principle: "Simple is better than complex"
"""
import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings, get_settings
from .logging_config import configure_logging
from .exception_handlers import register_exception_handlers
from .middleware import add_middlewares
from .routes import setup_frontend_routes

# Get a module-level logger
logger = logging.getLogger(__name__)


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Create and configure a FastAPI application.
    
    This function follows "Explicit is better than implicit" by clearly 
    showing each step of the application setup process.
    
    Args:
        settings: Optional Settings object, if None, loads from environment
        
    Returns:
        Configured FastAPI application 
    """
    # 1. Get settings (explicitly, no magic)
    if settings is None:
        settings = get_settings()
    
    # 2. Configure logging first (explicit, before any other operations)
    configure_logging(level=settings.LOG_LEVEL)
    logger.info("Creating application with settings: %s", settings.MODEL_DUMP_JSON(indent=2))
    
    # 3. Create the FastAPI app with explicit configuration
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API for Wedding RSVP and guest management",
        version="1.0.0",
        # Only show API docs in debug mode
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        debug=settings.DEBUG,
    )
    
    # 4. Register startup and shutdown events (simple, focused functions)
    @app.on_event("startup")
    async def startup_event():
        """Run when the application starts."""
        logger.info("Application startup")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        """Run when the application shuts down."""
        logger.info("Application shutdown")
    
    # 5. Register exception handlers
    register_exception_handlers(app)
    
    # 6. Add CORS middleware (explicit configuration)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 7. Add custom middlewares
    add_middlewares(app, settings)
    
    # 8. Setup frontend routes
    setup_frontend_routes(app)
    
    # 9. Setup API routes (explicit import here to avoid circular imports)
    from app.backend.api.router import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    # Log when the application is fully initialized
    logger.info(f"Application initialized: {settings.PROJECT_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    return app 