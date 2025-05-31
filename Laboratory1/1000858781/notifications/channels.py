import random
from abc import ABC, abstractmethod
from notifications.logger import NotificationLogger

class Notifier(ABC):
    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def notify(self, user, message, priority):
        """Attempts to send notification. Returns True if delivered, otherwise falls back to successor."""
        pass

class EmailNotifier(Notifier):
    def notify(self, user, message, priority):
        success = random.choice([True, False])
        NotificationLogger().log('email', user.name, success)
        if success:
            return True
        elif self._successor:
            return self._successor.notify(user, message, priority)
        return False

class SMSNotifier(Notifier):
    def notify(self, user, message, priority):
        success = random.choice([True, False])
        NotificationLogger().log('sms', user.name, success)
        if success:
            return True
        elif self._successor:
            return self._successor.notify(user, message, priority)
        return False

class ConsoleNotifier(Notifier):
    def notify(self, user, message, priority):
        # Console always succeeds for demonstration
        NotificationLogger().log('console', user.name, True)
        print(f"[Console] {user.name}: {message} (priority={priority})")
        return True
