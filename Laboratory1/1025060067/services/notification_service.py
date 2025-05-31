from models.user import User
from models.notification import Notification
from services.user_service import UserService
from utils.logger import Logger
from handlers.notification_handler import NotificationHandler
from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler
from strategies.notification_strategy import NotificationStrategy, HighPriorityStrategy, MediumPriorityStrategy, LowPriorityStrategy

class NotificationService:
    """
    Orchestrates the notification sending process,
    utilizing Chain of Responsibility and Strategy patterns.
    """
    def __init__(self, user_service: UserService):
        self._user_service = user_service
        self._channel_handlers: dict[str, NotificationHandler] = {
            "email": EmailHandler(),
            "sms": SMSHandler()
        }
        self._priority_strategies: dict[str, NotificationStrategy] = {
            "high": HighPriorityStrategy(),
            "medium": MediumPriorityStrategy(),
            "low": LowPriorityStrategy()
        }

    def _build_channel_chain(self, user: User) -> NotificationHandler | None:
        """
        Dynamically builds the Chain of Responsibility based on user's
        preferred and available channels.
        The preferred channel is always attempted first, followed by
        other available channels in their listed order.
        """
        # Ensure preferred channel is at the beginning of the available channels list
        ordered_channels = [user.preferred_channel] + [
            c for c in user.available_channels if c != user.preferred_channel
        ]

        head_handler = None
        current_handler = None

        for channel_name in ordered_channels:
            handler = self._channel_handlers.get(channel_name)
            if handler:
                if not head_handler:
                    head_handler = handler
                    current_handler = handler
                else:
                    current_handler.set_next(handler)
                    current_handler = handler
            else:
                Logger.log(f"Warning: Unknown channel handler for '{channel_name}'. Skipping.")
        return head_handler

    def _attempt_channel_delivery(self, user: User, message: str) -> bool:
        """
        Initiates the notification delivery process through the channel chain.
        """
        channel_chain = self._build_channel_chain(user)
        if channel_chain:
            Logger.log(f"Starting channel delivery chain for {user.name}...")
            return channel_chain.handle_notification(user, message)
        else:
            Logger.log(f"No valid notification channels configured for user {user.name}.")
            return False

    def send_notification(self, user_name: str, message: str, priority: str) -> dict:
        """
        Sends a notification to a user, using the appropriate strategy
        and triggering the channel delivery chain.
        """
        user = self._user_service.get_user(user_name)
        if not user:
            Logger.log(f"Error: User '{user_name}' not found for notification.")
            return {"status": "error", "message": f"User '{user_name}' not found."}

        strategy = self._priority_strategies.get(priority)
        if not strategy:
            Logger.log(f"Error: Invalid priority '{priority}' for notification.")
            return {"status": "error", "message": f"Invalid priority '{priority}'."}

        Logger.clear_logs() # Clear logs for each new notification attempt
        Logger.log(f"Initiating notification for '{user_name}' with '{priority}' priority.")
        
        delivery_successful = strategy.process_notification(user, message, self)
        
        if delivery_successful:
            Logger.log(f"Notification successfully delivered to {user.name}.")
            return {"status": "success", "message": "Notification sent successfully.", "logs": Logger.get_logs()}
        else:
            Logger.log(f"Notification delivery failed for {user.name} after all attempts.")
            return {"status": "failed", "message": "Notification delivery failed after all attempts.", "logs": Logger.get_logs()}
 