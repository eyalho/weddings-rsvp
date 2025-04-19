"""
Application entry point.
Creates and configures the FastAPI application.
"""
import os
import sys

# Make imports explicit and obvious - Zen: "Explicit is better than implicit"
# Add the parent directory to path to enable absolute imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Simple, direct import - Zen: "Simple is better than complex"
from app.backend.core.app_factory import create_app

# Create the application - no magic, just a simple factory call
app = create_app()

# Direct invocation for local development
if __name__ == "__main__":
    import uvicorn
    
    # Explicit configuration - Zen: "Explicit is better than implicit"
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )