from .base_handler import BaseHandler

class SmsHandler(BaseHandler):
    def channel_name(self) -> str:
        return "sms"
