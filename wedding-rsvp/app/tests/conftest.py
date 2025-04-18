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