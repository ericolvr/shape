""" configuration """
import logging
import sys
from typing import Optional
from app.config.config import get_settings

settings = get_settings()


def setup_logging() -> logging.Logger:
    """Configure and return the application logger"""
    
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("shape")
    logger.setLevel(log_level)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance"""
    if name:
        return logging.getLogger(f"shape.{name}")
    return logging.getLogger("shape")
