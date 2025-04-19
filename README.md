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