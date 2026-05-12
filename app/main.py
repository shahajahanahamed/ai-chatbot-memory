from fastapi import FastAPI

from app.core.config import get_settings
from app.api.v1.endpoint import router as chat_router
from app.db.redis_client import redis_client
from app.middleware.logging_middleware import add_request_id

settings = get_settings()

app = FastAPI(
    title="Chat with AI",
    version=settings.APP_VERSION,
    docs_url="/docs",          # Swagger UI
    redoc_url="/redoc",        # ReDoc UI
    openapi_url="/openapi.json"
)

# Adding the middleware to include request id
app.middleware("http")(add_request_id)

# Add version prefix here
app.include_router(
    chat_router,
    prefix="/api/v1",
    responses={
        200: {"description": "Ok"},
        404: {"description": "Not found"}
    }
)

@app.get("/health")
def health_check():
    try:
        redis_client.ping()
        return {"status": "ok", "redis": "connected"}
    except Exception:
        return {"status": "degraded", "redis": "down"}