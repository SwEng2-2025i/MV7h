from random import random

from src.core.handlers.handler import NotificationHandler
from src.core.logger.logger import Logger

logger = Logger()

import random 
class EmailHandler(NotificationHandler):
  def handle(self, notification) -> bool:
    state = random.choice([True, False])
    logger.log_action(notification, "email", state)
    if state:
      print(f"notification send through email")
      return True
    else:
      return super().handle(notification)