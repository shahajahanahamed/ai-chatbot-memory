from app.core.config import get_settings
from app.provider.groq_provider import GroqProvider
from app.provider.llm_provider import LLMProvider
from app.provider.openai_provider import OpenAIProvider
import logging
settings = get_settings()


logger = logging.getLogger(__name__)

class LLMFactory:

    @staticmethod
    def get_llm_provider() -> LLMProvider:
        provider = settings.LLM_PROVIDER.lower()

        logger.info(f"Selecting LLM provider: {provider}")

        if provider == "groq":
            return GroqProvider()
        elif provider == "openai":
            return OpenAIProvider()

        logger.error(f"Invalid LLM provider: {provider}")
        raise ValueError(f"Unsupported LLM provider: {provider}")