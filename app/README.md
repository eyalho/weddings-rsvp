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
```

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend API will be available at http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

## Development

This project uses:
- Backend: Python with FastAPI
- Frontend: React
- Database: [Your database choice] 