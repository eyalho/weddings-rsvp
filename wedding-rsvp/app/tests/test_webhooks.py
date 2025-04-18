import pytest

# Use the client fixture from conftest.py

def test_webhook_endpoint(client, test_webhook_payload):
    response = client.post("/api/v1/webhook", json=test_webhook_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "webhook processed"

def test_webhook_endpoint_invalid_payload(client):
    response = client.post("/api/v1/webhook", json=None)
    assert response.status_code == 422

def test_status_callback_endpoint(client, test_status_callback_payload):
    response = client.post("/api/v1/status_callback", json=test_status_callback_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "status callback processed"

def test_status_callback_invalid_payload(client):
    response = client.post("/api/v1/status_callback", json=None)
    assert response.status_code == 422