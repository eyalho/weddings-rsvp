#!/bin/bash
# Development script for the entire application (frontend + backend)

echo "====================================="
echo "Starting development environment"
echo "====================================="

# Navigate to the app directory
cd "$(dirname "$0")"
APP_DIR=$(pwd)

# Install backend dependencies
echo "Installing backend dependencies..."
cd "$APP_DIR/backend"
pip install -r requirements.txt
pip install -q uvicorn requests

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd "$APP_DIR/frontend"
npm install

# Start both services
echo "Starting development servers..."

# Start backend in background
cd "$APP_DIR/backend"
echo "Starting backend at http://localhost:8000"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment to ensure backend starts
sleep 2

# Start frontend
cd "$APP_DIR/frontend"
echo "Starting frontend at http://localhost:3000"
npm start

# Cleanup on exit
cleanup() {
    echo "Shutting down services..."
    kill $BACKEND_PID 2>/dev/null
    exit 0
}

# Set trap to catch SIGINT (Ctrl+C) and SIGTERM
trap cleanup SIGINT SIGTERM

# Wait for frontend to exit
wait 