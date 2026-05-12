from abc import ABC, abstractmethod
from typing import List, Dict

from app.schemas.chat_schema import ChatResponse


class LLMProvider(ABC):

    @abstractmethod
    def generate_with_history(self, user_id: int, messages: List[Dict[str, str]]) -> ChatResponse:
        """
        Generate response using conversation history.

        :param user_id: Unique user identifier (for logging & tracing)
        :param messages: List of chat messages (role + content)
        :return: ChatResponse
        """
        pass
