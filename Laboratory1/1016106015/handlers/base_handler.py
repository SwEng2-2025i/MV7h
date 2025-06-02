from abc import ABC, abstractmethod
import random
from log_util import logger

# Clase base abstracta para todos los manejadores de notificaciones
# Implementa el patrón Chain of Responsibility
class BaseHandler(ABC):
    def __init__(self, successor=None):
        # Cada manejador puede tener un sucesor en la cadena (el siguiente canal a intentar)
        self._successor = successor

    def handle(self, channel: str, user_name: str, message: str, priority: str):
        """
        Intenta manejar la notificación si el canal coincide.
        Si falla o no es su canal, pasa la solicitud al sucesor (siguiente en la cadena).

        Args:
            channel (str): Canal preferido del usuario (email o sms)
            user_name (str): Nombre del destinatario
            message (str): Contenido del mensaje
            priority (str): Prioridad del mensaje (no usada aquí, pero útil para extensión)

        Returns:
            bool: True si la entrega fue exitosa, False si todos fallaron
        """
        if channel == self.channel_name():
            # Simula aleatoriamente si el envío tiene éxito o falla
            success = random.choice([True, False])

            # Registra en el logger si se intentó y el resultado
            logger.log(f"Intentando {channel} para {user_name}: {'Éxito' if success else 'Fallo'}")

            # Si fue exitoso, se detiene la cadena
            if success:
                return True

        # Si no se pudo entregar o el canal no coincide, se pasa al siguiente manejador
        if self._successor:
            return self._successor.handle(channel, user_name, message, priority)

        # Si no hay más manejadores, se retorna False (fallo en todos los intentos)
        return False

    @abstractmethod
    def channel_name(self) -> str:
        """
        Debe ser implementado por subclases para indicar el nombre del canal que manejan.
        """
        pass
