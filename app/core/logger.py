

import logging
import sys

from app.core.config import get_settings


def setup_logger():
    settings = get_settings()
    log_level = settings.LOG_LEVEL.upper()
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    
def get_logger(name:str):
    return logging.getLogger(name)