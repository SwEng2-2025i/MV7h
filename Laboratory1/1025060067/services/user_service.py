from models.user import User
from models.notification import Notification
from utils.logger import Logger
from handlers.notification_handler import NotificationHandler
from handlers.email_handler import EmailHandler
from handlers.sms_handler import SMSHandler

class UserService:
    """
    Manages user registration and retrieval using in-memory data structures.
    """
    def __init__(self):
        self._users: dict[str, User] = {} # Stores users by name

    def register_user(self, name: str, preferred_channel: str, available_channels: list[str]) -> User:
        """
        Registers a new user. Raises ValueError if user already exists or data is invalid.
        """
        if name in self._users:
            raise ValueError(f"User with name '{name}' already exists.")
        
        user = User(name, preferred_channel, available_channels)
        self._users[name] = user
        Logger.log(f"User '{name}' registered successfully.")
        return user

    def get_user(self, name: str) -> User | None:
        """
        Retrieves a user by their name. Returns None if not found.
        """
        return self._users.get(name)

    def get_all_users(self) -> list[User]:
        """
        Retrieves a list of all registered users.
        """
        return list(self._users.values())

       
