from abc import ABC, abstractmethod

class BaseHandler(ABC):
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    @abstractmethod
    def handle(self, preferred, channels, user_name, message):
        pass
