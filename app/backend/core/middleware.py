"""
Application middleware module.

Contains streamlined middleware components following:
- "Simple is better than complex"
- "Readability counts"
- "Explicit is better than implicit"
"""
import time
import logging
from typing import Callable, List

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .config import Settings

# Module-level logger
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests.
    
    A simple, focused middleware that logs information about
    incoming requests and their responses.
    """
    
    def __init__(
        self, 
        app,
        exclude_paths: List[str] = None,
    ):
        """
        Initialize the middleware with explicit options.
        
        Args:
            app: The ASGI application
            exclude_paths: Path prefixes to exclude from logging
        """
        super().__init__(app)
        self.exclude_paths = exclude_paths or []
        
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log details about it.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            The response from downstream handlers
        """
        # Skip logging for excluded paths - explicit control
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Use simple, focused variables - "Readability counts"
        start_time = time.time()
        request_id = request.headers.get('X-Request-ID', '-')
        client_host = request.client.host if request.client else 'unknown'
        
        # Log the start of the request - keep it simple
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"[Client: {client_host}] [ID: {request_id}]"
        )
        
        try:
            # Process the request through the middleware chain
            response = await call_next(request)
            
            # Calculate and log request duration
            duration = time.time() - start_time
            logger.info(
                f"Response: {request.method} {request.url.path} "
                f"[Status: {response.status_code}] [Time: {duration:.4f}s] "
                f"[ID: {request_id}]"
            )
            
            return response
            
        except Exception as e:
            # Explicitly log errors - "Errors should never pass silently"
            duration = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url.path} "
                f"[Exception: {type(e).__name__}] [Time: {duration:.4f}s] "
                f"[ID: {request_id}]",
                exc_info=True
            )
            # Re-raise the exception - don't swallow errors
            raise


def add_middlewares(app: FastAPI, settings: Settings) -> None:
    """
    Add middlewares to the FastAPI application.
    
    Follows "Explicit is better than implicit" by making middleware 
    registration clear and centralized.
    
    Args:
        app: FastAPI application
        settings: Application settings
    """
    # Add request logging middleware
    app.add_middleware(
        RequestLoggingMiddleware,
        exclude_paths=[
            # Don't log health check or static file requests
            "/health",
            "/static",
            # Add more paths to exclude as needed
        ]
    )
    
    # Register additional middleware here as needed
    # app.add_middleware(...) 