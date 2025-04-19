import sys
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
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