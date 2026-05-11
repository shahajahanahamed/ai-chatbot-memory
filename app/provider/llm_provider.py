from abc import ABC, abstractmethod

from app.schemas.chat_schema import ChatResponse, ChatRequest


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, request:ChatRequest)->ChatResponse:
        pass
