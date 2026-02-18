"""background tasks for email"""
import time
from app.config.logging import get_logger

logger = get_logger("tasks.email")


def send_welcome_email(email: str, name: str):
    logger.info(f"Starting welcome email task: email={email}, name={name}")
    try:
        time.sleep(2)
        logger.info(f"Welcome email sent successfully: email={email}")
    except Exception as e:
        logger.error(f"Failed to send welcome email: email={email}, error={str(e)}")
        raise
