from fastapi import FastAPI
from .api.endpoints import webhooks
from .core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

# Include routers
app.include_router(webhooks.router, prefix=settings.API_V1_STR)