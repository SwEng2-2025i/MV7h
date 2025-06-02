import random
from services.handlers.base_handler import NotificationHandler
from logger import LoggerSingleton

class SmokeSignalHandler(NotificationHandler):
    def _handle(self, user, message):
        if "smoke" not in user.available_channels:
            return False

        logger = LoggerSingleton()
        logger.log(f"Trying smoke signals for {user.name}")

        success = random.choice([True, False])  # Simula si funciona o no
        if success:
            logger.log(f"Smoke signals sent to {user.name}: {message}")
            return True
        else:
            logger.log(f"Smoke signals failed for {user.name}")
            return False
