"""
Application entry point.
"""
import os
import sys

# Add the parent directories to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(app_dir)

# Add both paths for flexibility in imports
for path in [current_dir, app_dir, root_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Import app factory
from backend.core.app_factory import create_app

# Create the application
app = create_app()

# Direct invocation for local development
if __name__ == "__main__":
    import uvicorn
    
    # Run with uvicorn directly
    # Usage: python -m uvicorn backend.main:app --reload
    print("Run the app with: python -m uvicorn backend.main:app --reload")
    
    # For production:
    # gunicorn -w 1 -k uvicorn.workers.UvicornWorker --access-logfile - --error-logfile - --log-level debug backend.main:app
    
    # Default run configuration if script is executed directly
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )