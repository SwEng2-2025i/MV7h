from notifications.base_handler import NotificationHandler
from utils.logger import LoggerSingleton
import random

logger = LoggerSingleton()

# Cramos la clase simulada (según el resultado) para el canal de envio de correo
class EmailHandler(NotificationHandler):
    def handle(self, user, message):
        if "email" in user.available_channels:
            success = random.choice([True, False])
            # Añadimos al Logger para llevar un registro
            logger.log(user, "email", success)
            print("[EMAIL] Intentando enviar a", user.name, "-", "Éxito" if success else "Fallo")
            if success:
                return {"success": True, "channel": "email"}
        return self.try_next(user, message)
