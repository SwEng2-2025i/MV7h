from notifications.base_handler import NotificationHandler
from utils.logger import LoggerSingleton
import random

logger = LoggerSingleton()

# Cramos la clase simulada (según el resultado) para el canal de SMS
class SMSHandler(NotificationHandler):
    def handle(self, user, message):
        if "sms" in user.available_channels:
            success = random.choice([True, False])
            # Añadimos al Logger para llevar un registro
            logger.log(user, "SMS", success)
            # Usamos random para simular si el canal fue capaz o no
            print("[SMS] Intentando enviar a", user.name, "-", "Éxito" if success else "Fallo")
            if success:
                return {"success": True, "channel": "sms"}
        return self.try_next(user, message)
