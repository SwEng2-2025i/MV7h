# Un Logger muy sencillo implementado como Singleton

import threading  # Se usa para hacer thread-safe la creación de la instancia

class Logger:
    _instance = None             # Variable de clase que guarda la única instancia del Logger
    _lock = threading.Lock()     # Lock para garantizar que solo un hilo cree la instancia

    def __new__(cls):
        # Método especial que se llama antes de __init__, aquí se asegura que solo haya una instancia
        with cls._lock:  # Bloqueo para prevenir condiciones de carrera en entornos multihilo
            if cls._instance is None:
                # Si no existe la instancia, se crea y se asigna
                cls._instance = super().__new__(cls)
        # Retorna la instancia ya creada o recién creada
        return cls._instance

    def log(self, message: str):
        # Método público para registrar mensajes
        # En una implementación real escribiría en un archivo o sistema externo
        print(f"[LOG] {message}")  # Por simplicidad, imprime a consola

# Se instancia el logger (única vez gracias al Singleton)
logger = Logger()
