import logging
import sys

# Configure root logger to output to stdout
# This should be near the top of the file, before any imports that might configure logging
logging.basicConfig(
    level=logging.WARNING,  # Match your desired level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,  # Force output to stdout which Gunicorn can capture
    force=True  # Override any existing configuration
)

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from .api.endpoints import webhooks
from .core.config import settings

logger = logging.getLogger(__name__)
logger.info("Starting wedding RSVP API application")

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Include routers
app.include_router(webhooks.router, prefix=settings.API_V1_STR)

# Define frontend path - adjust this path as needed
frontend_build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "build"))

# Define the root route handler with conditional logic
@app.get("/", include_in_schema=False)
async def root():
    logger.info("Root endpoint accessed")
    if os.path.exists(frontend_build_path):
        logger.warning("Serving frontend index.html")
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
    else:
        logger.info("Serving API welcome message")
        return JSONResponse(content={"message": "Welcome to the wedding RSVP API"})

# Mount static files if build directory exists
if os.path.exists(frontend_build_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")
    
    @app.get("/{catch_all:path}", include_in_schema=False)
    async def serve_frontend_catchall(catch_all: str):
        # Exclude API routes
        if catch_all.startswith("api/"):
            logger.warning(f"API route not found: {catch_all}")
            raise HTTPException(status_code=404, detail="Not found")
        logger.info(f"Serving frontend for path: {catch_all}")
        return FileResponse(os.path.join(frontend_build_path, "index.html"))