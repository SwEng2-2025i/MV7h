from handlers.base_handler import BaseHandler
from logger.logger import Logger
import random

class EmailHandler(BaseHandler):
    def handle(self, preferred, channels, user_name, message):
        logger = Logger.get_instance()
        if "email" in channels:
            logger.log(f"Trying EMAIL for {user_name}")
            if random.choice([True, False]):
                logger.log(f"EMAIL sent to {user_name}: {message}")
                return True
            else:
                logger.log(f"EMAIL failed for {user_name}")
        if self.next_handler:
            return self.next_handler.handle(preferred, channels, user_name, message)
        return False
