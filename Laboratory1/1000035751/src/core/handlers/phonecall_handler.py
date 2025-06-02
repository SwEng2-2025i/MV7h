from random import random

from src.core.handlers.handler import NotificationHandler
from src.core.logger.logger import Logger

logger = Logger()

import random 
class PhonecallHandler(NotificationHandler):
  def handle(self, notification) -> bool:
    state = random.choice([True, False])
    logger.log_action(notification, "phonecall", state)
    if state:
      print(f"notification send through phonecall")
      return True
    else:
      return super().handle(notification)