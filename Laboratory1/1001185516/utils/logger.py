import threading

class LoggerSingleton:
    # Instancia única (singleton) y un lock para garantizar exclusividad en entornos con múltiples hilos
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Controla el acceso concurrente a la creación de la instancia
        with cls._lock:
            if cls._instance is None:
                # Si aún no existe, se crea la instancia y se inicializa la lista de logs
                cls._instance = super(LoggerSingleton, cls).__new__(cls)
                cls._instance.logs = []
            return cls._instance

    def log(self, user, channel, success):
        """
        Registra un intento de envío de notificación.
        :user: Nombre de usuario
        :Canal: Canal usado (email, sms, llamada)
        :Verificacion de exito: Booleano que indica si fue exitoso
        """
        entry = {
            "user": user.name,
            "channel": channel,
            "result": "Éxito" if success else "Fallo"
        }
        print(f"[LOGGER] {entry}")  # Muestra el logger por consola
        self.logs.append(entry)

    def get_logs(self):
        # Devuelve todos los registros almacenados hasta el momento.
        return self.logs