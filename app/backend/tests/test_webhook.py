"""
Tests for webhook endpoint functionality.
"""
import pytest
import os
import sys
import json
from fastapi.testclient import TestClient

# Add parent directories to sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

app_dir = os.path.dirname(backend_dir)
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Import app factory
from backend.core.app_factory import create_app
from backend.core.config import settings

@pytest.fixture
def client():
    """Test client fixture."""
    app = create_app()
    return TestClient(app)


def test_webhook_post_endpoint_json(client):
    """Test that the webhook POST endpoint accepts JSON."""
    test_data = {"test": True, "message": "Test webhook"}
    
    # Check with the API_V1_STR prefix
    response = client.post(
        f"{settings.API_V1_STR}/webhook",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    
    # Root endpoint test removed - only testing API prefixed endpoint

def test_webhook_post_endpoint_form(client):
    """Test that the webhook POST endpoint accepts form data."""
    test_data = {
        "From": "whatsapp:+1234567890",
        "To": "whatsapp:+0987654321",
        "Body": "Test message"
    }
    
    # Check with the API_V1_STR prefix
    response = client.post(
        f"{settings.API_V1_STR}/webhook",
        data=test_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    
    # Root endpoint test removed - only testing API prefixed endpoint 