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

app_dir = os.path.dirname(backend_dir)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import from correct location
from core.config import settings
from core.app_factory import create_app
from core.exceptions import AppException, NotFoundError

def test_app_initialization(client):
    """Test that the application initializes correctly."""
    # The client fixture already creates an app, just test its response
    response = client.get("/docs")
    assert response.status_code == 200  # DEBUG is True in test settings

def test_api_router_registration(client):
    """Test that API routers are registered correctly."""
    # Test the OpenAPI schema to ensure routes are registered
    openapi_response = client.get("/openapi.json")
    assert openapi_response.status_code == 200
    
    schema = openapi_response.json()
    # Check that webhook endpoints are in the schema
    webhook_path = "/webhook"
    assert webhook_path in schema["paths"]

def test_frontend_routes():
    """Test frontend route handling."""
    # Create an app with frontend routes enabled
    with patch('os.path.exists', return_value=True):
        test_settings = settings.model_copy(update={"DEBUG": True})
        app = create_app(test_settings)
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
    # Create a new app for this test specifically
    test_settings = settings.model_copy(update={"DEBUG": True})
    
    # Setup a fresh app with mocks to prevent frontend routes
    with patch('backend.core.routes.setup_frontend_routes') as mock_setup_frontend:
        # Mock the frontend setup function to do nothing
        mock_setup_frontend.return_value = None
        
        # Completely disable frontend routes by also mocking os.path.exists to return False
        # This prevents the frontend catchall route from being registered
        with patch('os.path.exists', return_value=False):
            # Create app with no frontend routes
            app = create_app(test_settings)
            
            # Define custom exception routes
            @app.get("/test-exception")
            def raise_app_exception():
                raise AppException(
                    status_code=400,
                    message="Test app exception",
                    error_code="TEST_ERROR"
                )
                
            @app.get("/test-not-found")
            def raise_not_found():
                raise NotFoundError(message="Test not found")
            
            client = TestClient(app)
            
            # Test app exception
            app_exc_response = client.get("/test-exception")
            assert app_exc_response.status_code == 400
            assert app_exc_response.json()["error"] == "TEST_ERROR"
            
            # Test not found error
            not_found_response = client.get("/test-not-found")
            assert not_found_response.status_code == 404
            assert not_found_response.json()["error"] == "NOT_FOUND" 