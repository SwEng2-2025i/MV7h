from domain.entities import User
from domain.notification_channels import EmailHandler, SMSHandler, ConsoleHandler

class NotificationUseCase:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register_user(self, name, preferred_channel, available_channels):
        user = User(name=name, preferred_channel=preferred_channel, available_channels=available_channels)
        self.user_repo.save(user)

    def get_all_users(self):
        return [user.__dict__ for user in self.user_repo.list_all()]

    def send_notification(self, user_name: str, message: str, priority: str = "normal") -> bool:
        user = self.user_repo.find_by_name(user_name)
        if not user:
            return False

        chain = self._build_chain(user.available_channels, user.preferred_channel)
        return chain.handle(message, user_name)

    def _build_chain(self, channels, preferred):
        channel_classes = {
            "email": EmailHandler,
            "sms": SMSHandler,
            "console": ConsoleHandler
        }

        sorted_channels = [preferred] + [c for c in channels if c != preferred]
        handler = None
        for ch in reversed(sorted_channels):
            handler = channel_classes[ch](next_handler=handler)
        return handler
