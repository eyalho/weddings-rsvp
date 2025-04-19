import pytest
from urllib.parse import urlencode

# Use the client fixture from conftest.py

def test_webhook_endpoint(client, test_webhook_payload):
    response = client.post("/api/v1/webhook", json=test_webhook_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "webhook processed"

def test_webhook_endpoint_invalid_payload(client):
    response = client.post("/api/v1/webhook", json=None)
    assert response.status_code in [200, 422]  # We now handle invalid JSON gracefully

def test_status_callback_endpoint(client, test_status_callback_payload):
    response = client.post("/api/v1/status_callback", json=test_status_callback_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "status callback processed"

def test_status_callback_invalid_payload(client):
    response = client.post("/api/v1/status_callback", json=None)
    assert response.status_code in [200, 422]  # We now handle invalid JSON gracefully

# WhatsApp message tests

def test_whatsapp_text_message(client, test_whatsapp_text_message):
    """Test WhatsApp text message in form-urlencoded format (typical from Twilio)"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # Convert dict to form-urlencoded format
    data = urlencode(test_whatsapp_text_message)
    
    response = client.post("/api/v1/webhook", data=data, headers=headers)
    assert response.status_code == 200
    
    # Should detect it as an RSVP based on the content
    assert response.json().get("message_type") == "rsvp"

def test_whatsapp_greeting(client, test_whatsapp_greeting):
    """Test WhatsApp greeting message"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = urlencode(test_whatsapp_greeting)
    
    response = client.post("/api/v1/webhook", data=data, headers=headers)
    assert response.status_code == 200
    
    # Should detect it as a greeting
    assert response.json().get("message_type") == "greeting"

def test_whatsapp_question(client, test_whatsapp_question):
    """Test WhatsApp question message"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = urlencode(test_whatsapp_question)
    
    response = client.post("/api/v1/webhook", data=data, headers=headers)
    assert response.status_code == 200
    
    # Should detect it as a question
    assert response.json().get("message_type") == "question"

def test_whatsapp_with_media(client, test_whatsapp_with_media):
    """Test WhatsApp message with media attachment"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = urlencode(test_whatsapp_with_media)
    
    response = client.post("/api/v1/webhook", data=data, headers=headers)
    assert response.status_code == 200
    
    # Should handle media message
    json_response = response.json()
    assert json_response["status"] in ["whatsapp_message_processed", "webhook processed"]

def test_empty_webhook(client):
    """Test empty webhook payload"""
    response = client.post("/api/v1/webhook", data="")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Empty request" in response.json()["message"]

def test_raw_string_webhook(client):
    """Test webhook with raw string data"""
    response = client.post("/api/v1/webhook", data="This is a test message")
    assert response.status_code == 200