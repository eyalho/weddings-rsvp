from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from .api.endpoints import webhooks
from .core.config import settings

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
    if os.path.exists(frontend_build_path):
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
    else:
        return JSONResponse(content={"message": "Welcome to the wedding RSVP API"})

# Mount static files if build directory exists
if os.path.exists(frontend_build_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")), name="static")
    
    @app.get("/{catch_all:path}", include_in_schema=False)
    async def serve_frontend_catchall(catch_all: str):
        # Exclude API routes
        if catch_all.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(os.path.join(frontend_build_path, "index.html"))