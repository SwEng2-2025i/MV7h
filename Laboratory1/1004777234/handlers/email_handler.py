from .base_handler import NotificationHandler

class EmailHandler(NotificationHandler):
    def __init__(self):
        super().__init__("email")