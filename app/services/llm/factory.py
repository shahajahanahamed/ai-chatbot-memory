
from app.core.config import get_settings
from app.services.llm.groq_provider import GroqProvider
from app.services.llm.llm_provider import BaseLLMProvider


settings = get_settings()

def get_llm_provider()->BaseLLMProvider:
    provider = settings.LLM_PROVIDER.lower()
    
    if(provider == "groq"):
        return GroqProvider()
    
    raise ValueError(f"Unsupported LLM provider: {provider}")