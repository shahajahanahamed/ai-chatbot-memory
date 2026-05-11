
from app.core.logger import get_logger
from app.services import llm
from app.services.llm.factory import get_llm_provider
logger = get_logger(__name__)

class ChatService:
   
    llm_provider = get_llm_provider()
    
    def get_response(self, message:str, user_id:str) -> str:
        logger.debug(f"Processing message | user_id={user_id} | message={message}")
        #Placeholder logic
        response = self.llm_provider.generate_response(message=message, user_id=user_id)
        logger.debug(f"Generated response | user_id={user_id}")
        return response