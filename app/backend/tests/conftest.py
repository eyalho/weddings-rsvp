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
        "SmsMessageSid": "SM95fd59caa1ad5c3138d42f804d9ffe04",
        "NumMedia": "0",
        "ProfileName": "Eyal",
        "MessageType": "text",
        "SmsSid": "SM95fd59caa1ad5c3138d42f804d9ffe04",
        "WaId": "972506228892",
        "SmsStatus": "received",
        "Body": "אישור הגעה",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGd48e1987c810083b6a6d18138f05fb68",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SM95fd59caa1ad5c3138d42f804d9ffe04",
        "AccountSid": "AC313eff5e520d98b7d65bc54c571b9712",
        "From": "whatsapp:+972506228892",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_greeting():
    """Example of a WhatsApp greeting message"""
    return {
        "SmsMessageSid": "SMa1b2c3d4e5f6g7h8i9j0",
        "NumMedia": "0",
        "ProfileName": "נועה",
        "MessageType": "text",
        "SmsSid": "SMa1b2c3d4e5f6g7h8i9j0",
        "WaId": "9725012345678",
        "SmsStatus": "received",
        "Body": "שלום",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGd48e1987c810083b6a6d18138f05fb68",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SMa1b2c3d4e5f6g7h8i9j0",
        "AccountSid": "AC313eff5e520d98b7d65bc54c571b9712",
        "From": "whatsapp:+9725012345678",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_question():
    """Example of a WhatsApp question message"""
    return {
        "SmsMessageSid": "SM123456789abcdef",
        "NumMedia": "0",
        "ProfileName": "דניאל",
        "MessageType": "text",
        "SmsSid": "SM123456789abcdef",
        "WaId": "9725098765432",
        "SmsStatus": "received",
        "Body": "האם יש חניה באולם?",
        "To": "whatsapp:+972509518554",
        "MessagingServiceSid": "MGd48e1987c810083b6a6d18138f05fb68",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "SM123456789abcdef",
        "AccountSid": "AC313eff5e520d98b7d65bc54c571b9712",
        "From": "whatsapp:+9725098765432",
        "ApiVersion": "2010-04-01"
    }

@pytest.fixture
def test_whatsapp_with_media():
    """Example of a WhatsApp message with media attached"""
    return {
        "SmsMessageSid": "MMabcdef123456789",
        "NumMedia": "1",
        "ProfileName": "מיכל",
        "MessageType": "text",
        "SmsSid": "MMabcdef123456789",
        "WaId": "9725054321123",
        "SmsStatus": "received",
        "Body": "",
        "To": "whatsapp:+972509518554",
        "MediaContentType0": "image/jpeg",
        "MediaUrl0": "https://api.twilio.com/2010-04-01/Accounts/AC313eff5e520d98b7d65bc54c571b9712/Messages/MMabcdef123456789/Media/ME123456",
        "MessagingServiceSid": "MGd48e1987c810083b6a6d18138f05fb68",
        "NumSegments": "1",
        "ReferralNumMedia": "0",
        "MessageSid": "MMabcdef123456789",
        "AccountSid": "AC313eff5e520d98b7d65bc54c571b9712",
        "From": "whatsapp:+9725054321123",
        "ApiVersion": "2010-04-01"
    }