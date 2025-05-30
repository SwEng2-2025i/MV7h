import random
from logger import Logger

class NotificationHandler:
    def __init__(self, channel):
        self.channel = channel
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle(self, user, message):
        if self.channel in user.available_channels:
            Logger().log(f"Trying {self.channel} for {user.name}")
            success = random.choice([True, False])
            if success:
                Logger().log(f"Delivered via {self.channel}")
                return {"status": "success", "channel": self.channel}
            else:
                Logger().log(f"{self.channel} failed for {user.name}")
        if self.next_handler:
            return self.next_handler.handle(user, message)
        return {"status": "failed", "reason": "All channels failed"}