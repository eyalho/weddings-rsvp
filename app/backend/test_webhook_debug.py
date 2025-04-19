"""
Debug script for webhook handling.

This script helps diagnose issues with webhook processing
by creating test payloads and checking the service's processing logic.
"""
import json
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Add parent directory to import path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import the webhook service
from services.webhook_service import handle_webhook, webhook_service

# Test payloads
test_cases = [
    {
        "name": "WhatsApp Form Data",
        "payload": {
            "type": "whatsapp",
            "message": {
                "from": "+1234567890",
                "to": "+9876543210",
                "body": "Hello from form data",
                "profile_name": "TestUser",
                "media_count": "0"
            },
            "form_data": {
                "SmsMessageSid": "SM123",
                "NumMedia": "0",
                "ProfileName": "TestUser",
                "MessageType": "text",
                "SmsSid": "SM123",
                "WaId": "1234567890",
                "SmsStatus": "received",
                "Body": "Hello from form data",
                "To": "whatsapp:+9876543210",
                "MessageSid": "SM123",
                "From": "whatsapp:+1234567890"
            }
        }
    },
    {
        "name": "WhatsApp JSON Format",
        "payload": {
            "type": "whatsapp",
            "message": {
                "from": "+1234567890",
                "to": "+9876543210",
                "body": "Hello from JSON",
                "profile_name": "JSONUser",
                "media_count": "0"
            },
            "form_data": {
                "MessageSid": "SM456",
                "WaId": "1234567890", 
                "SmsStatus": "received"
            }
        }
    },
    {
        "name": "Generic JSON Webhook",
        "payload": {
            "test": True,
            "message": "Test webhook",
            "timestamp": "2023-04-19T12:00:00Z"
        }
    }
]

def main():
    """Run the webhook debug tests."""
    print("\n===== WEBHOOK DEBUG TEST =====")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n----- Test Case {i}: {test_case['name']} -----")
        payload = test_case["payload"]
        
        print(f"Input payload: {json.dumps(payload, indent=2)}")
        print(f"Payload type: {type(payload)}")
        print(f"Has 'type' key: {'type' in payload}")
        if 'type' in payload:
            print(f"Type value: '{payload['type']}'")
        print(f"Has 'message' key: {'message' in payload}")
        
        print("\nCalling webhook_service.process_webhook directly:")
        response = webhook_service.process_webhook(payload)
        print(f"Response: {json.dumps(response, indent=2)}")
        
        print("\nCalling handle_webhook function:")
        response2 = handle_webhook(payload)
        print(f"Response: {json.dumps(response2, indent=2)}")
        
        print("\n")

if __name__ == "__main__":
    main() 