from langchain_groq import ChatGroq
from pydantic import SecretStr

from app.core.config import get_settings
from app.services.llm.llm_provider import BaseLLMProvider

settings = get_settings()

class GroqProvider(BaseLLMProvider):
    
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY
        )
        
    def generate_response(self, message: str, user_id: str) -> str:
        response = self.llm.invoke(message)
        content = response.content
        
        if isinstance(content, str):
            return content
        
        return str(content)
        
    