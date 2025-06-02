from notifications.base_handler import NotificationHandler
from utils.logger import LoggerSingleton
import random

logger = LoggerSingleton()

# Cramos la clase simulada (según el resultado) para el canal de llamada
class CallHandler(NotificationHandler):
    def handle(self, user, message):
        if "llamada" in user.available_channels:
            success = random.choice([True, False])
            # Añadimos al Logger para llevar un registro
            logger.log(user, "llamada", success)
            # Usamos random para simular si el canal fue capaz o no
            print("[LLAMADA] Intentando llamar a", user.name, "-", "Éxito" if success else "Fallo")
            if success:
                return {"success": True, "channel": "llamada"}
        return self.try_next(user, message)
