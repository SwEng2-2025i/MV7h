import random
from .base_handler import NotificationHandler
from logger import LoggerSingleton


class EmailHandler(NotificationHandler):
    def _handle(self, user, message):
        if "email" not in user.available_channels:
            return False

        logger = LoggerSingleton()
        logger.log(f"Trying email for {user.name}")

        success = random.choice([True, False])
        if success:
            logger.log(f"Email sent to {user.name}: {message}")
            return True
        else:
            logger.log(f"Email failed for {user.name}")
            return False
