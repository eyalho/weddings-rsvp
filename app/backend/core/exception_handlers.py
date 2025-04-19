"""
Exception handlers module.

Defines handlers for application exceptions, following the principles:
- "Errors should never pass silently"
- "Unless explicitly silenced"
- "Explicit is better than implicit"
"""
import logging
import traceback
from typing import Dict, Any, Type, Callable

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from .exceptions import AppException

# Set up module logger
logger = logging.getLogger(__name__)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handler for application-specific exceptions.
    
    Makes error handling explicit by:
    1. Logging the error with appropriate level
    2. Returning a structured response with clear error details
    
    Args:
        request: The request that caused the exception
        exc: The caught exception
        
    Returns:
        JSONResponse with error details
    """
    # Log with appropriate level based on status code
    log_msg = f"AppException: {exc.message} - Code: {exc.error_code} - Status: {exc.status_code}"
    if exc.status_code >= 500:
        logger.error(log_msg)
    else:
        logger.warning(log_msg)
    
    # Return structured error response
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "path": request.url.path
        }
    )

async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError | ValidationError
) -> JSONResponse:
    """
    Handler for request validation errors.
    
    Makes validation errors explicit by:
    1. Logging the validation errors
    2. Returning a structured response with detailed validation errors
    
    Args:
        request: The request that caused the exception
        exc: The validation exception
        
    Returns:
        JSONResponse with validation error details
    """
    # Get errors
    if hasattr(exc, 'errors'):
        errors = exc.errors()
    else:
        errors = [{"msg": str(exc)}]
        
    # Log the validation errors
    logger.warning(
        f"Validation error at {request.url.path}: {errors}"
    )
    
    # Return structured validation error response
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": errors,
            "path": request.url.path
        }
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for unhandled exceptions.
    
    Follows "Errors should never pass silently" by:
    1. Logging the full exception with traceback
    2. Returning a clear server error response
    
    Args:
        request: The request that caused the exception
        exc: The caught exception
        
    Returns:
        JSONResponse with error info
    """
    # Log the exception with traceback for debugging
    logger.error(
        f"Unhandled exception in {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    # In development mode, include more details
    from .config import get_settings
    settings = get_settings()
    
    content = {
        "error": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred",
        "path": request.url.path
    }
    
    # Only include exception details in debug mode
    if settings.DEBUG:
        content["details"] = {
            "exception": str(exc),
            "traceback": traceback.format_exc().split("\n")
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content
    )

def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers with the FastAPI application.
    
    Makes error handling setup explicit by centralizing all registrations.
    
    Args:
        app: FastAPI application
    """
    # Register application-specific exception handlers
    app.add_exception_handler(AppException, app_exception_handler)
    
    # Register validation exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    
    # Register catch-all exception handler - "Errors should never pass silently"
    app.add_exception_handler(Exception, generic_exception_handler) 