from abc import ABC, abstractmethod

class NotificationHandler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, next_handler):
        self._next = next_handler
        return next_handler

    def handle(self, user, message):
        success = self._handle(user, message)
        if not success and self._next:
            return self._next.handle(user, message)
        return success

    @abstractmethod
    def _handle(self, user, message):
        pass
