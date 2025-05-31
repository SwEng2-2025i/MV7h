from utils.logger import Logger
from models.user import User
from handlers.notification_handler import NotificationHandler

class EmailHandler(NotificationHandler):
    """
    Concrete handler for email notifications.
    """
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Handles email notification. If successful, stops the chain.
        If failed, passes to the next handler if available.
        """
        if self._simulate_delivery("email", user.name):
            Logger.log(f"Notification sent successfully to {user.name} via Email: '{message}'")
            return True
        elif self._next_handler:
            Logger.log(f"Email delivery failed for {user.name}. Trying next channel...")
            return self._next_handler.handle_notification(user, message)
        else:
            Logger.log(f"Email delivery failed for {user.name} and no more handlers in chain.")
            return False
