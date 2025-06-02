from canales.correo import CanalCorreo
from canales.sms import CanalSMS
from canales.consola import CanalConsola

def construir_cadena(usuario):
    canales_map = {
        "correo": CanalCorreo,
        "sms": CanalSMS,
        "consola": CanalConsola
    }

    canales = [canales_map[n]() for n in usuario.canales_disponibles]
    for i in range(len(canales) - 1):
        canales[i].set_siguiente(canales[i+1])
    return canales[0]

def notificar_usuario(usuario, mensaje):
    inicio = construir_cadena(usuario)
    return inicio.enviar(usuario, mensaje)
