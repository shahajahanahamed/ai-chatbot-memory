import json
import logging
from typing import List, Dict

from app.db.redis_client import redis_client

logger = logging.getLogger(__name__)


class MemoryService:

    @staticmethod
    def get_history(user_id: int) -> List[Dict[str, str]]:
        try:
            data = redis_client.get(f"chat:{user_id}")

            if not data:
                return []

            return json.loads(data)

        except Exception:
            logger.exception(
                "Redis error while fetching history",
                extra={"user_id": user_id}
            )

            # ✅ fallback: no memory instead of crashing
            return []

    @staticmethod
    def save_message(user_id: int, role: str, content: str):
        try:
            history = MemoryService.get_history(user_id)

            history.append({
                "role": role,
                "content": content
            })

            redis_client.set(
                f"chat:{user_id}",
                json.dumps(history),
                ex=3600
            )

        except Exception:
            logger.exception(
                "Redis error while saving message",
                extra={"user_id": user_id}
            )