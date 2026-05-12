import logging
from typing import List, Dict

from langchain_groq import ChatGroq

from app.core.config import get_settings
from app.provider.llm_provider import LLMProvider
from app.schemas.chat_schema import ChatResponse

logger = logging.getLogger(__name__)
settings = get_settings()


class GroqProvider(LLMProvider):

    def __init__(self):
        try:
            self.llm = ChatGroq(
                api_key=settings.GROQ_API_KEY.get_secret_value(),
                model=settings.GROQ_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                max_retries=3,
            )
            logger.info("GroqProvider initialized successfully")

        except Exception:
            logger.exception("Failed to initialize GroqProvider")
            raise

    def generate_with_history(self, user_id: int, messages: List[Dict[str, str]]) -> ChatResponse:

        logger.info("LLM request started", extra={"user_id": user_id, "message_count": len(messages)})

        try:
            # Call LLM
            response = self.llm.invoke(messages)

            if not response or not response.content:
                logger.warning("Empty response from LLM", extra={"user_id": user_id})
                return ChatResponse(can_answer=False, actual_answer="No response generated")

            logger.debug("LLM response generated", extra={"user_id": user_id, "response_length": len(response.content)})

            return ChatResponse(can_answer=True, actual_answer=response.content)

        except Exception:
            logger.exception("Error while generating LLM response", extra={"user_id": user_id})

            return ChatResponse(can_answer=False, actual_answer="Something went wrong. Please try again later.")
