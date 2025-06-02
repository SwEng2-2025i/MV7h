class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message: str):
        print(f"[LOG] {message}")
        self.logs.append(message)

    def get_logs(self):
        return self.logs.copy()