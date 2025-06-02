from abc import ABC, abstractmethod
from typing import Optional


class BaseHandler(ABC):
    def __init__(self, successor: Optional["BaseHandler"] = None):
        self._successor = successor

    def set_successor(self, successor: "BaseHandler"):
        self._successor = successor

    @abstractmethod
    def handle(self, notification: dict) -> bool:
        """
        Intenta enviar la notificación por este canal.
        Retorna True si tuvo éxito, False de lo contrario (para pasar al siguiente).
        """
        pass
