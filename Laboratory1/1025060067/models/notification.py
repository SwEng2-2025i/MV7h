import uuid

class Notification:
    """
    Represents a notification to be sent.
    """
    def __init__(self, user_name: str, message: str, priority: str):
        if not user_name or not isinstance(user_name, str):
            raise ValueError("User name must be a non-empty string.")
        if not message or not isinstance(message, str):
            raise ValueError("Message must be a non-empty string.")
        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be 'high', 'medium', or 'low'.")

        self.user_name = user_name
        self.message = message
        self.priority = priority

    def to_dict(self) -> dict:
        """
        Converts the Notification object to a dictionary.
        """
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority
        }