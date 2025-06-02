import abc
import random
from utils.logger import Logger
from models.user import User

class NotificationHandler(abc.ABC):
    """
    Abstract base class for notification channel handlers.
    Implements the Chain of Responsibility pattern.
    """
    def __init__(self):
        self._next_handler: NotificationHandler = None

    def set_next(self, handler: "NotificationHandler") -> "NotificationHandler":
        """
        Sets the next handler in the chain.
        """
        self._next_handler = handler
        return handler

    @abc.abstractmethod
    def handle_notification(self, user: User, message: str) -> bool:
        """
        Abstract method to handle a notification attempt for a specific channel.
        Returns True if delivery was successful, False otherwise.
        """
        pass

    def _simulate_delivery(self, channel_name: str, user_name: str) -> bool:
        """
        Simulates the delivery attempt for a channel.
        Randomly returns True for success or False for failure.
        Logs the attempt and result.
        """
        success = random.choice([True, False]) # Simulate random failure
        if success:
            Logger.log(f"Attempting to send notification to {user_name} via {channel_name} - SUCCESS")
        else:
            Logger.log(f"Attempting to send notification to {user_name} via {channel_name} - FAILED")
        return success


