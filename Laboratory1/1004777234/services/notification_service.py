from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler
from models.notification import Notification

class NotificationService:
    def send_notification(self, user, message, priority):
        notification = Notification(user, message, priority)

        # Build the chain
        handler_map = {
            "email": EmailHandler(),
            "sms": SMSHandler(),
        }

        first_handler = handler_map[user.preferred_channel]
        current = first_handler
        for channel in user.available_channels:
            if channel != user.preferred_channel:
                current = current.set_next(handler_map[channel])

        return first_handler.handle(user, message)