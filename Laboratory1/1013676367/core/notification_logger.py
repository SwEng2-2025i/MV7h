import json
import os
from datetime import datetime
from contextlib import contextmanager

class NotificationLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.log_file = "notification_logs.json"
        self._ensure_log_file()

    def _ensure_log_file(self):
        try:
            with self._open_log_file('r') as f:
                json.load(f) 
        except (FileNotFoundError, json.JSONDecodeError):
            with self._open_log_file('w') as f:
                json.dump([], f) 

    @contextmanager
    def _open_log_file(self, mode):
        try:
            with open(self.log_file, mode, encoding='utf-8') as f:
                yield f
        except IOError as e:
            print(f"Error al abrir al archivo: {str(e)}")
            raise

    def _read_logs(self):
        try:
            with self._open_log_file('r') as f:
                return json.load(f) if os.path.getsize(self.log_file) > 0 else []
        except (json.JSONDecodeError, IOError):
            return []

    def _write_logs(self, logs):
        try:
            with self._open_log_file('w') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"🚨 No se pudieron guardar: {str(e)}")

    def log_attempt(self, user, channel, message, state):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user.name,
            "channel": channel,
            "message": message,
            "success": state
        }
        
        logs = self._read_logs()
        logs.append(log_entry)
        self._write_logs(logs)

    def get_logs(self):
        return self._read_logs()