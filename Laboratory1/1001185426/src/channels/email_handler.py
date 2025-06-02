import random
from src.channels.base_handler import BaseHandler


class EmailHandler(BaseHandler):
    def __init__(self, successor=None):
        super().__init__(successor)

    def handle(self, notification: dict) -> bool:
        success = random.choice([True, False])
        if success:
            print(f"[EMAIL] Notificación a {notification['user_name']}: {notification['message']}")
            return True
        else:
            print(f"[EMAIL] Falló envío por email. Pasando a siguiente canal...")
            if self._successor:
                return self._successor.handle(notification)
            return False
