from .base_handler import BaseHandler

class EmailHandler(BaseHandler):
    def channel_name(self) -> str:
        return "email"
