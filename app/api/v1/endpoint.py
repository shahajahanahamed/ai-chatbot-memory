

from fastapi import APIRouter

from app.core.logger import get_logger
from app.models.chat_model import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chats"]
)

logger = get_logger(__name__)

chat_service = ChatService()

@router.post(path="",response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"Incoming request | user_id={request.user_id}")
    try:
        response = chat_service.get_response(message=request.message, user_id=request.user_id)
        logger.info(f"Response generated | user_id={request.user_id}")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing request | user_id={request.user_id} | error={str(e)}")
        raise e
    
    