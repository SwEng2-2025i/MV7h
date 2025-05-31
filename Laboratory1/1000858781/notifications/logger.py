import threading

class NotificationLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def log(self, channel, user, success):
        print(f"[LOG] Canal={channel} Usuario={user} Success={success}")