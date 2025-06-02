from utils.logger import Logger
from models.user import User
from handlers.notification_handler import NotificationHandler

class SMSHandler(NotificationHandler):
    """
    Concrete handler for SMS notifications.
    """
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Handles SMS notification. If successful, stops the chain.
        If failed, passes to the next handler if available.
        """
        if self._simulate_delivery("sms", user.name):
            Logger.log(f"Notification sent successfully to {user.name} via SMS: '{message}'")
            return True
        elif self._next_handler:
            Logger.log(f"SMS delivery failed for {user.name}. Trying next channel...")
            return self._next_handler.handle_notification(user, message)
        else:
            Logger.log(f"SMS delivery failed for {user.name} and no more handlers in chain.")
            return False
        