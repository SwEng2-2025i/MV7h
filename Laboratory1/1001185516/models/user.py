#Definimos el JSON de entrada, dando las claves de los canales preferidos y los disponibles

class User:
    def __init__(self, name: str, preferred_channel: str, available_channels: list[str]):
        self.name = name
        self.preferred_channel = preferred_channel
        self.available_channels = available_channels
