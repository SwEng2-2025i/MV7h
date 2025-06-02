from abc import ABC, abstractmethod

class CanalNotificacion(ABC):
    def __init__(self):
        self.siguiente = None

    def set_siguiente(self, canal):
        self.siguiente = canal

    @abstractmethod
    def enviar(self, usuario, mensaje):
        pass
