import random
from services.handlers.base_handler import NotificationHandler
from logger import LoggerSingleton

class SMSHandler(NotificationHandler):
    def _handle(self, user, message):
        if "sms" not in user.available_channels:
            return False

        logger = LoggerSingleton()
        logger.log(f"Trying SMS for {user.name}")

        success = random.choice([True, False])
        if success:
            logger.log(f"SMS sent to {user.name}: {message}")
            return True
        else:
            logger.log(f"SMS failed for {user.name}")
            return False
