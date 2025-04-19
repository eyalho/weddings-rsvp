#!/bin/bash
# Restart script for the backend service

echo "====================================="
echo "Preparing and restarting application"
echo "====================================="

# Navigate to the backend directory
cd "$(dirname "$0")"
BACKEND_DIR=$(pwd)
APP_DIR=$(dirname "$BACKEND_DIR")

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Preparing frontend..."
cd "$APP_DIR/frontend"
npm install
npm run build

echo "Returning to backend directory..."
cd "$BACKEND_DIR"

# Find and stop the running service
echo "Checking for existing processes..."
PID=$(ps -ef | grep "backend.main:app" | grep -v grep | awk '{print $2}')
if [ ! -z "$PID" ]; then
    echo "Stopping existing process (PID: $PID)"
    kill $PID
    sleep 2
fi

# Make sure we have dependencies
echo "Checking additional dependencies..."
pip install -q gunicorn uvicorn requests

# Start the service
echo "Starting service in production mode..."
nohup gunicorn -w 1 -k uvicorn.workers.UvicornWorker \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    backend.main:app > server.log 2>&1 &

NEW_PID=$!
echo "Service started with PID: $NEW_PID"

# Wait a moment for the service to start
sleep 3

# Test the webhook endpoint
echo "Testing webhook endpoints..."
python test_webhook.py

echo "Deployment complete." 