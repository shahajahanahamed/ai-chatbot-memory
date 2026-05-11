import logging

from app.factory.factory import LLMFactory
from app.schemas.chat_schema import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)


class ChatService:
    _provider = None  # class-level cache

    def __init__(self):
        if not ChatService._provider:
            try:
                ChatService._provider = LLMFactory.get_llm_provider()
                logger.info("LLM Provider initialized once")
            except Exception:
                logger.exception("Failed to initialize provider")
                raise

        self.provider = ChatService._provider

    def generate_response(self, request: ChatRequest) -> ChatResponse:
        logger.info(f"Processing request | user_id={request.user_id}")

        try:
            response = self.provider.generate(request)

            logger.info(
                f"Response generated | user_id={request.user_id} | can_answer={response.can_answer}"
            )

            return response

        except Exception:
            logger.exception(
                f"Error in ChatService | user_id={request.user_id}"
            )

            return ChatResponse(
                can_answer=False,
                actual_answer="Internal server error"
            )