from fastapi import FastAPI

from app.core.config import get_settings
from app.api.v1.endpoint import router as chat_router

settings = get_settings()

app = FastAPI(
    title="Chat with AI",
    version=settings.APP_VERSION,
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc",        # ReDoc UI
    openapi_url="/openapi.json"
)

# Add version prefix here
app.include_router(
    chat_router,
    prefix="/api/v1",
    responses={
        200: {"description": "Ok"},
        404: {"description": "Not found"}
    }
)