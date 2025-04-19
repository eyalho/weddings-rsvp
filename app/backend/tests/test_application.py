"""
Tests for the application structure and initialization.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add parent directories to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Use relative imports
from core.startup import init_app
from core.config import settings

def test_app_initialization():
    """Test that the application initializes correctly."""
    with patch('core.startup.setup_logging'):
        app = init_app()
        assert app.title == settings.PROJECT_NAME
        assert app.debug == settings.DEBUG
        
        client = TestClient(app)
        response = client.get("/docs")
        assert response.status_code == 200 if settings.DEBUG else 404

def test_api_router_registration():
    """Test that API routers are registered correctly."""
    with patch('core.startup.setup_logging'):
        app = init_app()
        client = TestClient(app)
        
        # Test the OpenAPI schema to ensure routes are registered
        openapi_response = client.get("/openapi.json")
        if not settings.DEBUG:
            assert openapi_response.status_code == 404
            return
            
        assert openapi_response.status_code == 200
        schema = openapi_response.json()
        
        # Check that webhook endpoints are in the schema
        webhook_path = f"{settings.API_V1_STR}/webhook"
        assert webhook_path in schema["paths"]

def test_frontend_routes():
    """Test frontend route handling."""
    with patch('core.startup.setup_logging'), \
         patch('os.path.exists', return_value=True), \
         patch('core.routes.FileResponse', return_value={"dummy": "response"}):
        app = init_app()
        client = TestClient(app)
        
        # Test root route
        root_response = client.get("/")
        assert root_response.status_code == 200
        
        # Test SPA route handling
        spa_response = client.get("/some/frontend/route")
        assert spa_response.status_code == 200
        
        # Test API 404 handling
        api_response = client.get(f"{settings.API_V1_STR}/nonexistent")
        assert api_response.status_code == 404

def test_exception_handling():
    """Test that exception handlers work correctly."""
    with patch('core.startup.setup_logging'):
        from core.exceptions import AppException, NotFoundError
        
        app = init_app()
        
        @app.get("/test/app-exception")
        def raise_app_exception():
            raise AppException(
                status_code=400,
                message="Test app exception",
                error_code="TEST_ERROR"
            )
            
        @app.get("/test/not-found")
        def raise_not_found():
            raise NotFoundError(message="Test not found")
        
        client = TestClient(app)
        
        # Test app exception
        app_exc_response = client.get("/test/app-exception")
        assert app_exc_response.status_code == 400
        assert app_exc_response.json()["error"] == "TEST_ERROR"
        
        # Test not found error
        not_found_response = client.get("/test/not-found")
        assert not_found_response.status_code == 404
        assert not_found_response.json()["error"] == "NOT_FOUND" 