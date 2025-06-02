from src.channels.base_handler import BaseHandler


class ConsoleHandler(BaseHandler):
    def __init__(self, successor=None):
        super().__init__(successor)

    def handle(self, notification: dict) -> bool:
        # Como canal de última instancia, asumimos que imprimir en consola siempre "funciona"
        print(f"[CONSOLE] Notificación para {notification['user_name']}: {notification['message']} (Canal fallback)")
        return True
