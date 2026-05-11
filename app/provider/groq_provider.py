import logging
from typing import Optional

from langchain_groq import ChatGroq

from app.core.config import get_settings
from app.provider.llm_provider import LLMProvider
from app.schemas.chat_schema import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)
settings = get_settings()


class GroqProvider(LLMProvider):

    def __init__(self):
        try:
            self.llm = ChatGroq(
                api_key=settings.GROQ_API_KEY,
                model=settings.GROQ_MODEL,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS,
                max_retries=3,
            )
            logger.info("GroqProvider initialized successfully")
        except Exception as e:
            logger.exception("Failed to initialize GroqProvider")
            raise


    def generate(self, request: ChatRequest) -> ChatResponse:
        logger.info(f"Request received | user_id={request.user_id}")

        try:
            # Call LLM
            response = self.llm.invoke(request.query)

            if not response or not response.content:
                logger.warning(f"Empty response from LLM | user_id={request.user_id}")
                return ChatResponse(
                    can_answer=False,
                    actual_answer="No response generated"
                )

            logger.debug(
                f"LLM response generated | user_id={request.user_id} | "
                f"response_length={len(response.content)}"
            )

            return ChatResponse(
                can_answer=True,
                actual_answer=response.content
            )

        except Exception as e:
            logger.exception(
                f"Error while generating response | user_id={request.user_id}"
            )

            return ChatResponse(
                can_answer=False,
                actual_answer="Something went wrong. Please try again later."
            )