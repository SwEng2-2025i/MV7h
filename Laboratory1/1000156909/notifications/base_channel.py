import random
from utils.logger import Logger

class NotificationChannel:
    def __init__(self):
        self.next = None
        self.logger = Logger.get_instance()

    def set_next(self, next_channel):
        self.next = next_channel
        return next_channel

    def handle(self, message, user_name):
        raise NotImplementedError