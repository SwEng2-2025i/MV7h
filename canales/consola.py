import random
from canales.canal_base import CanalNotificacion
from patrones.singleton_logger import Logger

class CanalConsola(CanalNotificacion):
    def enviar(self, usuario, mensaje):
        Logger().log(f"[Consola] Intentando enviar a {usuario.nombre}")
        if random.choice([True, False]):
            Logger().log(f"[Consola] Enviado a {usuario.nombre}")
            return True
        Logger().log(f"[Consola] Falló al enviar a {usuario.nombre}")
        if self.siguiente:
            return self.siguiente.enviar(usuario, mensaje)
        return False
