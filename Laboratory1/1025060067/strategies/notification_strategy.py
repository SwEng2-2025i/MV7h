import abc
from utils.logger import Logger
from models.user import User 

# Forward declaration for type hinting NotificationService
# This avoids circular import issues between services.py and strategies.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from services import NotificationService

class NotificationStrategy(abc.ABC):
    """
    Abstract base class for notification priority strategies.
    Implements the Strategy pattern.
    """
    @abc.abstractmethod
    def process_notification(self, user: User, message: str, notification_service: "NotificationService") -> bool:
        """
        Processes the notification based on its priority.
        """
        pass

class HighPriorityStrategy(NotificationStrategy):
    """
    Strategy for high priority notifications.
    """
    def process_notification(self, user: User, message: str, notification_service: "NotificationService") -> bool:
        Logger.log(f"Processing HIGH priority notification for {user.name}.")
        # High priority might have specific retry logic or logging, but for this lab,
        # it primarily orchestrates the channel delivery.
        return notification_service._attempt_channel_delivery(user, message)

class MediumPriorityStrategy(NotificationStrategy):
    """
    Strategy for medium priority notifications.
    """
    def process_notification(self, user: User, message: str, notification_service: "NotificationService") -> bool:
        Logger.log(f"Processing MEDIUM priority notification for {user.name}.")
        return notification_service._attempt_channel_delivery(user, message)

class LowPriorityStrategy(NotificationStrategy):
    """
    Strategy for low priority notifications.
    """
    def process_notification(self, user: User, message: str, notification_service: "NotificationService") -> bool:
        Logger.log(f"Processing LOW priority notification for {user.name}.")
        return notification_service._attempt_channel_delivery(user, message)
