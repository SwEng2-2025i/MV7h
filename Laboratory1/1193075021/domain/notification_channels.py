import random
from abc import ABC, abstractmethod
from domain.logger_singleton import LoggerSingleton

class NotificationHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler
        self.logger = LoggerSingleton()

    def handle(self, message: str, user_name: str):
        if self.try_send(message, user_name):
            self.logger.log(f"Sent to {self.__class__.__name__} for user {user_name}")
            return True
        elif self.next_handler:
            self.logger.log(f"Failed on {self.__class__.__name__}, trying next")
            return self.next_handler.handle(message, user_name)
        else:
            self.logger.log("All channels failed.")
            return False

    @abstractmethod
    def try_send(self, message: str, user_name: str) -> bool:
        pass


class EmailHandler(NotificationHandler):
    def try_send(self, message: str, user_name: str) -> bool:
        return random.choice([True, False])


class SMSHandler(NotificationHandler):
    def try_send(self, message: str, user_name: str) -> bool:
        return random.choice([True, False])


class ConsoleHandler(NotificationHandler):
    def try_send(self, message: str, user_name: str) -> bool:
        print(f"[Console] {user_name}: {message}")
        return True
