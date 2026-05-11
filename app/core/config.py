from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Chatbot"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    LLM_PROVIDER:str="groq"
    LLM_TEMPERATURE:float = 0.1
    LLM_MAX_TOKENS:int = 1000
    
    GROQ_API_KEY: SecretStr
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    
    

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()