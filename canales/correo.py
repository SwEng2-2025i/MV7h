import random
from canales.canal_base import CanalNotificacion
from patrones.singleton_logger import Logger

class CanalCorreo(CanalNotificacion):
    def enviar(self, usuario, mensaje):
        Logger().log(f"[Correo] Intentando enviar a {usuario.nombre}")
        if random.choice([True, False]):
            Logger().log(f"[Correo] Enviado a {usuario.nombre}")
            return True
        Logger().log(f"[Correo] Falló al enviar a {usuario.nombre}")
        if self.siguiente:
            return self.siguiente.enviar(usuario, mensaje)
        return False
