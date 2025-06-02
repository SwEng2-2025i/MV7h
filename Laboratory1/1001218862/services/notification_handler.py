import random
from services.logger import Logger

class NotificationHandler:
    def __init__(self, channel_name):
        self._next_handler = None
        self.channel_name = channel_name
        self.logger = Logger()

    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, notification):
        user = notification.user

        if self.channel_name in user.available_channels:
            self.logger.log(f"Attempting {self.channel_name} for {user.name}")
            if random.random() < 0.7: # 50% de posibilidades de fallar
                self.logger.log(f"{self.channel_name} notification sent to {user.name}")
                return True
            else:
                self.logger.log(f"{self.channel_name} failed for {user.name}")

        if self._next_handler:
            return self._next_handler.handle(notification)
        else:
            self.logger.log(f"All channels failed for {user.name}")
            return False

class EmailHandler(NotificationHandler):
    def __init__(self):
        super().__init__('email')

class SMSHandler(NotificationHandler):
    def __init__(self):
        super().__init__('sms')
