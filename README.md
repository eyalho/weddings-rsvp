# Wedding RSVP Application

A full-stack application for managing wedding RSVPs.

## Project Structure

```
/
├── .github/             # GitHub Actions workflows
├── app/
│   ├── backend/         # Python backend API
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   ├── services/    # Business logic services
│   │   └── tests/       # Unit and integration tests
│   └── frontend/        # React frontend
│       ├── public/      # Static assets
│       └── src/         # React source code
```

## Getting Started

### Backend Setup
```bash
cd app/backend
pip install -r requirements.txt
python main.py
```

The backend API will be available at http://localhost:8000

### Frontend Setup
```bash
cd app/frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

## Python Import Patterns

The backend uses two import approaches depending on the context:

1. **Relative imports** within the backend package:
   ```python
   from ..core.config import settings  # From api module to core module
   from .middleware import RequestLoggingMiddleware  # Within same module
   ```

2. **Absolute imports** when needed (with proper Python path setup):
   ```python
   # Setting up Python path in main.py
   import os, sys
   root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
   sys.path.insert(0, root_dir)
   
   # Then imports can work
   from app.backend.core.app_factory import create_app
   ```

## CI/CD

This project uses GitHub Actions for continuous integration. The workflow:
- Runs backend tests
- Builds and tests the frontend
- Ensures code quality

The workflow configuration is in `.github/workflows/ci.yml`.

## Development

This project uses:
- Backend: Python with FastAPI
- Frontend: React
- Database: SQLite (development) / PostgreSQL (production)

## Running Tests

```bash
# From project root
python -m pytest app/backend/tests -v

# From backend directory
cd app/backend
python -m pytest tests -v
```