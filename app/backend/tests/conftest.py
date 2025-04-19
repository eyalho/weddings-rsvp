import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add the app directory to Python path for potential imports that use app.* structure
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Add the project root directory to Python path
root_dir = os.path.dirname(app_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import directly from backend
from backend.core.app_factory import create_app
from backend.core.config import settings

@pytest.fixture
def client():
    """Create a test client with a fresh FastAPI app instance optimized for testing."""
    # Create test settings with DEBUG enabled
    test_settings = settings.model_copy(update={
        "DEBUG": True,
    })
    
    # Setup a fresh app with mocks to prevent frontend routes from being registered
    with patch('backend.core.routes.setup_frontend_routes') as mock_setup_frontend:
        # Mock the frontend setup function to do nothing
        mock_setup_frontend.return_value = None
        
        # Create app with no frontend routes
        app = create_app(test_settings)
        
        # Import the API router directly
        from backend.api.router import api_router
        
        # Mount the API router at root level for easier testing
        app.include_router(api_router)
        
        # Return the test client
        return TestClient(app)

@pytest.fixture
def test_webhook_payload():
    return {"test": "data"}

@pytest.fixture
def test_status_callback_payload():
    return {"status": "completed"}

@pytest.fixture
def test_whatsapp_text_message():
    """Example of a WhatsApp text message from Twilio"""
    return {
        "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumMedia": "0",
        "ProfileName": "Eyal",
        "MessageType": "text",
        "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "WaId": "972506228892",
        "SmsStatus": "received",
        "Body": "אישור הגעה",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "From": "whatsapp:+972506228892",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_greeting():
    """Example of a WhatsApp greeting message"""
    return {
        "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumMedia": "0",
        "ProfileName": "נועה",
        "MessageType": "text",
        "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "WaId": "9725012345678",
        "SmsStatus": "received",
        "Body": "שלום",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "From": "whatsapp:+9725012345678",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_question():
    """Example of a WhatsApp question message"""
    return {
        "SmsMessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumMedia": "0",
        "ProfileName": "דניאל",
        "MessageType": "text",
        "SmsSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "WaId": "9725098765432",
        "SmsStatus": "received",
        "Body": "האם יש חניה באולם?",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "From": "whatsapp:+9725098765432",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_with_media():
    """Example of a WhatsApp message with media attached"""
    return {
        "SmsMessageSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumMedia": "1",
        "ProfileName": "מיכל",
        "MessageType": "text",
        "SmsSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "WaId": "9725054321123",
        "SmsStatus": "received",
        "Body": "",
        "To": "whatsapp:+972509518554",
        "MediaContentType0": "image/jpeg",
        "MediaUrl0": "https://example.com/api/2010-04-01/Accounts/ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/Messages/MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/Media/MExxxx",
        "MessagingServiceSid": "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "MMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "AccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "From": "whatsapp:+9725054321123",
        "ApiVersion": "2010-04-01"
    }