"""
Application exception handling.
Define custom exceptions and exception handlers for the application.
"""
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)

class AppException(Exception):
    """Base exception for application-specific errors."""
    def __init__(
        self, 
        status_code: int,
        message: str,
        error_code: str = "APP_ERROR",
        details: dict = None
    ):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class WebhookException(AppException):
    """Exception raised for webhook processing errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="WEBHOOK_ERROR",
            details=details
        )

class NotFoundError(AppException):
    """Exception raised when a resource is not found."""
    def __init__(self, message: str = "Resource not found", details: dict = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="NOT_FOUND",
            details=details
        )

# Exception handlers

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handler for application-specific exceptions."""
    logger.warning(
        f"AppException: {exc.message} - Code: {exc.error_code} - Status: {exc.status_code}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

async def validation_exception_handler(
    request: Request, 
    exc: RequestValidationError
) -> JSONResponse:
    """Handler for request validation errors."""
    errors = exc.errors()
    logger.warning(f"Validation error: {errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": errors
        }
    )

async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unhandled exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred"
        }
    ) 