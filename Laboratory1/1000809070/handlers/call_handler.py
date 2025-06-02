from handlers.base_handler import BaseHandler
from logger.logger import Logger
import random

class CallHandler(BaseHandler):
    def handle(self, preferred, channels, user_name, message):
        logger = Logger.get_instance()
        if "call" in channels:
            logger.log(f"Trying CALL for {user_name}")
            if random.choice([True, False]):
                logger.log(f"CALL sent to {user_name}: {message}")
                return True
            else:
                logger.log(f"CALL failed for {user_name}")
        logger.log(f"All channels failed for {user_name}")
        return False
