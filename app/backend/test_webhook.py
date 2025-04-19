#!/usr/bin/env python
"""
Simple webhook testing utility.
"""
import requests
import json
import sys

def test_webhook_get(url="http://localhost:8000/api/v1/webhook"):
    """Test if the webhook endpoint is accessible via GET."""
    print(f"Testing webhook GET endpoint at {url}")
    
    try:
        response = requests.get(url)
        print(f"GET Response status: {response.status_code}")
        
        try:
            print(f"GET Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"GET Response text: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"GET Error: {str(e)}")
        return False

def test_webhook_post(url="http://localhost:8000/api/v1/webhook"):
    """Test if the webhook endpoint accepts POST requests."""
    print(f"Testing webhook POST endpoint at {url}")
    
    try:
        # Test with JSON payload
        test_data = {
            "test": True, 
            "message": "Test webhook payload",
            "timestamp": "2023-01-01T12:00:00Z"
        }
        
        response = requests.post(
            url, 
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"POST Response status: {response.status_code}")
        
        try:
            print(f"POST Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"POST Response text: {response.text}")
            
        # Also test with form data
        form_data = {
            "From": "whatsapp:+1234567890",
            "To": "whatsapp:+0987654321",
            "Body": "Test message",
            "MessageSid": "SM123456",
            "ProfileName": "Test User"
        }
        
        print(f"Testing webhook POST with form data")
        form_response = requests.post(
            url, 
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        print(f"Form POST Response status: {form_response.status_code}")
        
        try:
            print(f"Form POST Response: {json.dumps(form_response.json(), indent=2)}")
        except:
            print(f"Form POST Response text: {form_response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"POST Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Use command line arguments if provided
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/api/v1/webhook"
    method = sys.argv[2].upper() if len(sys.argv) > 2 else "BOTH"
    
    success = True
    
    if method == "GET" or method == "BOTH":
        get_success = test_webhook_get(url)
        if not get_success:
            success = False
            print("❌ Webhook GET test failed!")
        else:
            print("✅ Webhook GET test succeeded!")
    
    if method == "POST" or method == "BOTH":
        post_success = test_webhook_post(url)
        if not post_success:
            success = False
            print("❌ Webhook POST test failed!")
        else:
            print("✅ Webhook POST test succeeded!")
    
    if success:
        print("All webhook tests passed!")
        sys.exit(0)
    else:
        print("Some webhook tests failed!")
        sys.exit(1) 