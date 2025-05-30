from .base_handler import NotificationHandler

class SMSHandler(NotificationHandler):
    def __init__(self):
        super().__init__("sms")