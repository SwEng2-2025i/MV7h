# Iniciamos la cadena de responsabilidad
class NotificationHandler:
    def __init__(self):
        self.next_handler = None
    # Primer intento

    def set_next(self, handler):
        self.next_handler = handler
        return handler
    # Segundo intento

    def handle(self, user, message):
        raise NotImplementedError("Debe implementarse en la subclase")
    # Mensaje de error para prueba

    def try_next(self, user, message):
        if self.next_handler:
            return self.next_handler.handle(user, message)
        else:
            return {"success": False, "channel": None, "error": "Todos los canales fallaron"}
    # Tercer intento y error (solo tenemos 3 canales)
