import json
import logging
from typing import List, Dict

from app.db.redis_client import redis_client

logger = logging.getLogger(__name__)


class MemoryService:

    TTL_SECONDS = 3600
    MAX_MESSAGES = 10  # prevent infinite growth

    @staticmethod
    def _get_key(user_id: int, session_id: str) -> str:
        """
        Build Redis key using user_id + session_id
        Example: chat:1:abc123
        """
        return f"chat:{user_id}:{session_id}"

    @staticmethod
    def get_history(user_id: int, session_id: str) -> List[Dict[str, str]]:
        try:
            key = MemoryService._get_key(user_id, session_id)

            data = redis_client.get(key)

            if not data:
                return []

            history = json.loads(data)

            return history

        except Exception:
            logger.exception(
                "Error fetching history from Redis",
                extra={"user_id": user_id, "session_id": session_id}
            )
            return []

    @staticmethod
    def save_message(user_id: int, session_id: str, role: str, content: str):
        try:
            key = MemoryService._get_key(user_id, session_id)

            history = MemoryService.get_history(user_id, session_id)

            # Add new message
            history.append({
                "role": role,
                "content": content
            })

            # Trim history (important)
            if len(history) > MemoryService.MAX_MESSAGES:
                history = history[-MemoryService.MAX_MESSAGES:]

            redis_client.set(
                key,
                json.dumps(history),
                ex=MemoryService.TTL_SECONDS
            )

        except Exception:
            logger.exception(
                "Error saving message to Redis",
                extra={"user_id": user_id, "session_id": session_id}
            )

    @staticmethod
    def clear_history(user_id: int, session_id: str):
        try:
            key = MemoryService._get_key(user_id, session_id)
            redis_client.delete(key)

        except Exception:
            logger.exception(
                "Error clearing history",
                extra={"user_id": user_id, "session_id": session_id}
            )