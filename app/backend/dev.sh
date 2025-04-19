#!/bin/bash
# Development script for running the backend in development mode

echo "Starting backend in development mode..."

# Navigate to the backend directory
cd "$(dirname "$0")"

# Ensure we have the necessary dependencies
pip install -q uvicorn requests

# Run with hot reload enabled
echo "Running with hot reload at http://localhost:8000"
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 