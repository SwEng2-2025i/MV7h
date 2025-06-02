class Logger:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(Logger, cls).__new__(cls)
            cls._instancia.historial = []
        return cls._instancia

    def log(self, mensaje):
        print(mensaje)
        self.historial.append(mensaje)

    def obtener_logs(self):
        return self.historial
