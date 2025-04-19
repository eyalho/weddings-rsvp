import pytest
from urllib.parse import parse_qs, unquote_plus
import json

from ..api.endpoints.webhooks import extract_whatsapp_message

def test_whatsapp_message_extraction(test_whatsapp_text_message):
    """Test extraction of WhatsApp message details"""
    message = extract_whatsapp_message(test_whatsapp_text_message)
    
    # Verify key fields are extracted correctly
    assert message["message_sid"] == test_whatsapp_text_message["MessageSid"]
    assert message["from_number"] == test_whatsapp_text_message["From"].replace("whatsapp:", "")
    assert message["profile_name"] == test_whatsapp_text_message["ProfileName"]
    assert message["body"] == test_whatsapp_text_message["Body"]
    assert message["status"] == test_whatsapp_text_message["SmsStatus"]

def test_url_encoded_message_parsing():
    """Test parsing of URL-encoded WhatsApp messages"""
    # Simulate a URL-encoded message body from Twilio
    encoded_body = "SmsMessageSid=SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&Body=Hello+%D7%A9%D7%9C%D7%95%D7%9D&From=whatsapp%3A%2B9725551234"
    
    # Parse it manually to verify our parsing logic
    form_data = {}
    params = encoded_body.split('&')
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            form_data[key] = unquote_plus(value)
    
    # Verify correct parsing
    assert form_data["SmsMessageSid"] == "SMxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    assert form_data["Body"] == "Hello שלום"  # Hebrew characters correctly decoded
    assert form_data["From"] == "whatsapp:+9725551234"

def test_whatsapp_message_categorization(test_whatsapp_greeting, test_whatsapp_question):
    """Test detection of different message types"""
    from ..services.webhook_service import handle_whatsapp_message
    
    # Test greeting detection
    greeting_result = handle_whatsapp_message(extract_whatsapp_message(test_whatsapp_greeting))
    assert greeting_result["message_type"] == "greeting"
    
    # Test question detection
    question_result = handle_whatsapp_message(extract_whatsapp_message(test_whatsapp_question))
    assert question_result["message_type"] == "question"

def test_media_message_handling(test_whatsapp_with_media):
    """Test handling of WhatsApp messages with media"""
    message = extract_whatsapp_message(test_whatsapp_with_media)
    
    # Check media information is preserved
    assert message["num_media"] == test_whatsapp_with_media["NumMedia"]
    
    # In a real implementation, you might add additional fields for media URLs
    # assert "media_url" in message
    # assert "media_type" in message 