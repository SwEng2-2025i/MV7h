from .base_channel import NotificationChannel
import random

class SMSChannel(NotificationChannel):
    def handle(self, message, user_name):
        success = random.choice([True, False])
        self.logger.log(f"SMS attempt for {user_name}: {'Success' if success else 'Failure'}")
        if success:
            return f"Notification sent to {user_name} via SMS"
        elif self.next:
            return self.next.handle(message, user_name)
        else:
            return f"All channels failed for {user_name}"