from contextlib import asynccontextmanager
from logging import getLogger
from fastapi import FastAPI

from app.api.v1.endpoint import router as chat_router
from app.core.logger import setup_logger

# 1. Initialize your custom logging configuration
setup_logger()
logger = getLogger(__name__)

# 2. Define the Lifespan manager (Replaces startup/shutdown events)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on Startup
    logger.info("🚀 Application started")
    
    yield  # The app is "alive" here
    
    # This runs on Shutdown
    logger.info("🛑 Application shutting down")

# 3. Initialize FastAPI with the lifespan
app = FastAPI(
    title="AI Chatbot with Memory",
    version="0.0.1",
    lifespan=lifespan
)

# 4. Include Routers
app.include_router(chat_router, prefix="/api/v1")
