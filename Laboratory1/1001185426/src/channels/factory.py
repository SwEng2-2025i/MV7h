from src.channels.email_handler import EmailHandler
from src.channels.sms_handler import SMSHandler
from src.channels.console_handler import ConsoleHandler


class HandlerFactory:
    @staticmethod
    def get_chain(preferred: str, available: list[str]):
        """
        Devuelve el primer handler (canal preferido), encadenado con los demás disponibles.
        E.g., preferred="email", available=["email","sms","console"]
        """
        # Creamos un diccionario que mapea nombre de canal a clase de Handler
        mapping = {
            "email": EmailHandler,
            "sms": SMSHandler,
            "console": ConsoleHandler
        }

        # Validar que preferred esté en available
        if preferred not in available:
            raise ValueError(f"El canal preferido '{preferred}' no está en la lista de disponibles {available}")

        # Construimos la lista de clases en el orden: primero preferred, luego el resto sin repetir
        order = [preferred] + [c for c in available if c != preferred]

        # Instanciamos la cadena: empezamos por el final (último fallback), y vamos envolviendo
        chain = None
        # Recorremos al revés para ir formando: C3 -> C2(C3) -> C1(C2->C3)
        for canal in reversed(order):
            HandlerClass = mapping.get(canal.lower())
            if HandlerClass is None:
                continue  # ignoramos canales desconocidos
            chain = HandlerClass(successor=chain)
        return chain
