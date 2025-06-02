from random import random

from src.core.handlers.handler import NotificationHandler
from src.core.logger.logger import Logger

logger = Logger()

import random 
class SmsHandler(NotificationHandler):
  def handle(self, notification) -> str:
    state = random.choice([True, False])
    logger.log_action(notification, "sms", state)
    if state:
      print(f"notification send through sms")
      return True
    else:
      return super().handle(notification)