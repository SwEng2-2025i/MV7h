# Importa los manejadores concretos de notificación
from .email_handler import EmailHandler
from .sms_handler import SmsHandler

def build_chain(channels: list):
    """
    Construye la cadena de responsabilidad a partir de una lista de canales.
    
    Cada canal se mapea a su clase manejadora correspondiente.
    La cadena se construye en orden inverso para que el primer canal preferido
    sea el primero en intentar entregar la notificación.
    
    Args:
        channels (list): Lista ordenada de canales (ej. ["email", "sms"])

    Returns:
        Instancia del primer manejador en la cadena.
    """

    # Diccionario que mapea nombres de canal a su clase manejadora
    mapping = {
        "email": EmailHandler,
        "sms": SmsHandler
    }

    chain = None  # La cadena comienza vacía

    # Se recorre la lista de canales en orden inverso para encadenar correctamente
    for ch in reversed(channels):
        HandlerClass = mapping.get(ch)  # Se obtiene la clase correspondiente al canal
        if HandlerClass:
            # Se crea una nueva instancia del manejador, apuntando al siguiente (el chain actual)
            chain = HandlerClass(successor=chain)

    # Retorna la cabeza de la cadena de responsabilidad
    return chain
