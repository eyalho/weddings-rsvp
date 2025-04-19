# Wedding RSVP Application

This is a full-stack application for managing wedding RSVPs.

## Project Structure

```
app/
├── backend/             # Python backend API
│   ├── api/             # API endpoints
│   ├── core/            # Core functionality
│   ├── services/        # Business logic services
│   └── tests/           # Unit and integration tests
├── frontend/            # React frontend
│   ├── public/          # Static assets
│   └── src/             # React source code
├── dev.sh               # Development script for both frontend and backend
```

## Quick Start

### Development Mode (Recommended)

Run both frontend and backend with a single command:

```bash
# From the app directory
./dev.sh
```

This will:
1. Install all dependencies for backend and frontend
2. Start the backend server at http://localhost:8000
3. Start the frontend dev server at http://localhost:3000

### Production Deployment

Deploy the complete application:

```bash
# From the backend directory
cd backend
./restart.sh
```

This will:
1. Install backend dependencies
2. Install frontend dependencies and build for production
3. Restart the backend server using gunicorn

## Manual Setup

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Development mode
python -m uvicorn backend.main:app --reload

# Production mode
gunicorn -w 1 -k uvicorn.workers.UvicornWorker --log-level debug backend.main:app
```

The backend API will be available at http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install

# Development mode
npm start

# Production build
npm run build
```

The frontend will be available at http://localhost:3000

## Development

This project uses:
- Backend: Python with FastAPI
- Frontend: React
- Database: SQLite (development) / PostgreSQL (production) 