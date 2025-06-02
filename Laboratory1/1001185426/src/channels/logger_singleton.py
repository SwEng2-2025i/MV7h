import threading


class NotificationLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NotificationLogger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file: str = "notifications.log"):
        # Pues solo inicializamos una vez
        if self._initialized:
            return
        self.log_file = log_file
        # Abrimos el archivo en modo append
        self._file_handle = open(self.log_file, "a")
        self._initialized = True

    def log(self, text: str):
        self._file_handle.write(text + "\n")
        self._file_handle.flush()

    def __del__(self):
        if hasattr(self, "_file_handle"):
            self._file_handle.close()
