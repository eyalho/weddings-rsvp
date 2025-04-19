# Backend - Wedding RSVP Application

FastAPI backend service for the Wedding RSVP application.

## Directory Structure

```
backend/
├── api/              # API routes and endpoint definitions
├── core/             # Core functionality (config, security, etc.)
├── db/               # Database models and connection handling
├── services/         # Business logic services
├── tests/            # Unit and integration tests
├── main.py           # Application entry point
└── requirements.txt  # Python dependencies
```

## Setup and Installation

```bash
# Navigate to the backend directory
cd app/backend

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the automatically generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Main API Endpoints

- `GET /api/health` - Health check endpoint
- `POST /api/rsvp` - Submit RSVP information
- `GET /api/rsvp/{id}` - Get RSVP information by ID
- `GET /api/rsvp/list` - Get list of all RSVPs

## Webhook Endpoints

The application provides webhook endpoints for integrating with external services like Twilio:

- `POST /api/v1/webhook` - Main webhook endpoint for incoming messages
- `POST /api/v1/status_callback` - Status callback endpoint for message delivery updates

You can test these endpoints with:

```bash
# Test webhook endpoint
curl -X GET http://localhost:8000/api/v1/webhook

# Test status callback endpoint
curl -X GET http://localhost:8000/api/v1/status_callback
```

These webhook endpoints are available at both:
- `/api/v1/webhook` (direct access) 
- `/api/v1/webhooks/webhook` (via API router)

Both routes are supported for compatibility with different integrations.

## Development Guidelines

### Import Pattern

Use relative imports when possible:

```python
# Within the same module
from .config import settings

# Between modules
from ..api.endpoints import router
```

### Adding New Endpoints

1. Create a new router file in `api/` directory
2. Define your routes and handlers
3. Import and include the router in `main.py`

### Database Models

Add new models in the `db/models.py` file and ensure they follow the SQLAlchemy ORM pattern.

### Running Tests

```bash
# Run all tests
python -m pytest tests -v

# Run specific test file
python -m pytest tests/test_api.py -v
```

## Running the Application

### Development Mode

For development with hot-reload:

```bash
# Using the convenience script
./dev.sh

# Or manually
python -m uvicorn backend.main:app --reload
```

### Production Mode

For production with Gunicorn:

```bash
# Using the restart script
./restart.sh

# Or manually with Gunicorn
gunicorn -w 1 -k uvicorn.workers.UvicornWorker --access-logfile - --error-logfile - --log-level debug backend.main:app
```

## Testing Webhooks

Test both GET and POST webhook endpoints with:

```bash
# Test both GET and POST
python test_webhook.py

# Test only GET
python test_webhook.py http://localhost:8000/api/v1/webhook GET

# Test only POST
python test_webhook.py http://localhost:8000/api/v1/webhook POST
```

The script will test JSON and form data POST requests to ensure all webhook functionality works correctly. 