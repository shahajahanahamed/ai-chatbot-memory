
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_response(self, message:str, user_id:str)->str:
        pass