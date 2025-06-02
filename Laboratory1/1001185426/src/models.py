class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: list[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels

    def to_dict(self):
        return {
            "name": self.name,
            "preferred_channel": self.preferred_channel,
            "available_channels": self.available_channels
        }


class Notification:
    def __init__(self, user_name: str, message: str, priority: str):
        self.user_name = user_name
        self.message = message
        self.priority = priority

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }
