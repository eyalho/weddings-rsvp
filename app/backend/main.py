"""
Application entry point.
Creates and configures the FastAPI application.
"""
import os
import sys

# Make imports explicit and obvious - Zen: "Explicit is better than implicit"
# Add the root directory to path to enable absolute imports
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# This allows imports from the 'app' package
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Simple, direct import - Zen: "Simple is better than complex"
from backend.core.app_factory import create_app

# Create the application - no magic, just a simple factory call
app = create_app()

# Direct invocation for local development
if __name__ == "__main__":
    import uvicorn
    
    # Explicit configuration - Zen: "Explicit is better than implicit"
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )