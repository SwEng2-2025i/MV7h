# Importamos todos nuestros servicios de notificación
# Revisamos nuestra base de memoria para verificar si el usuario realmente esta

from notifications.email_handler import EmailHandler
from notifications.sms_handler import SMSHandler
from notifications.call_handler import CallHandler
from services.user_service import get_user

# Enviamos la notificacion en caso de encontrar al usuario
def send_notification(user_name, message):
    user = get_user(user_name)
    if not user:
        return {"error": "Usuario no encontrado"}, 404

    # Crear y ordenar la cadena según la prioridad del usuario
    handlers_map = {
        "email": EmailHandler(),
        "sms": SMSHandler(),
        "llamada": CallHandler()
    }

    ordered_handlers = [handlers_map[ch] for ch in user.available_channels if ch in handlers_map]
    # Creamos una lista segun la preferencia de los handlers

    for i in range(len(ordered_handlers) - 1):
        ordered_handlers[i].set_next(ordered_handlers[i + 1])
    # Genera la cadena de responsabilidad iterando entre las opciones posibles

    first_handler = handlers_map.get(user.preferred_channel, ordered_handlers[0])
    # Se intenta usar el canal preferido ingresado por el usuario

    resultado = first_handler.handle(user, message)
    # Dispara el proceso de notificación
    return resultado
