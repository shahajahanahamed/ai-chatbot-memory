import logging
from typing import List, Dict

from app.factory.factory import LLMFactory
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.memory_service import MemoryService

logger = logging.getLogger(__name__)


class ChatService:
    _provider = None  # Singleton-like cache

    def __init__(self):
        if not ChatService._provider:
            try:
                ChatService._provider = LLMFactory.get_llm_provider()
                logger.info("LLM Provider initialized (singleton)")
            except Exception:
                logger.exception("Failed to initialize LLM provider")
                raise

        self.provider = ChatService._provider

    def generate_response(self, request: ChatRequest) -> ChatResponse:
        user_id = request.user_id

        logger.info("Processing chat request", extra={"user_id": user_id})

        try:
            # 1. Fetch history
            history: List[Dict[str, str]] = MemoryService.get_history(user_id)

            logger.debug("Fetched conversation history", extra={"user_id": user_id, "history_length": len(history)})

            # 2. Build message payload
            messages = [
                           {"role": "system", "content": "You are a helpful AI assistant."}
                       ] + history + [
                           {"role": "user", "content": request.query}
                       ]

            # 3. Generate response from LLM
            response = self.provider.generate_with_history(
                user_id=user_id,
                messages=messages
            )

            # 4. Persist conversation (only if valid response)
            if response.can_answer:
                MemoryService.save_message(user_id, "user", request.query)
                MemoryService.save_message(user_id, "assistant", response.actual_answer)

                logger.debug("Conversation saved to memory", extra={"user_id": user_id})

            logger.info("Response generated successfully",
                        extra={"user_id": user_id, "can_answer": response.can_answer})

            return response

        except Exception:
            logger.exception("Error in ChatService", extra={"user_id": user_id})

            return ChatResponse(can_answer=False, actual_answer="Internal server error")
