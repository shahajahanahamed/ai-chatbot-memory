import logging
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

logger = logging.getLogger(__name__)
chat_service = ChatService()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:

    logger.info(f"Request received | user_id={request.user_id}")
    logger.debug(f"Query: {request.query[:100]}")

    try:
        response = await run_in_threadpool(
            chat_service.generate_response, request
        )

        logger.info(
            f"Request completed | user_id={request.user_id} | can_answer={response.can_answer}"
        )

        return response

    except Exception:
        logger.exception(
            f"Unhandled error in endpoint | user_id={request.user_id}"
        )

        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )