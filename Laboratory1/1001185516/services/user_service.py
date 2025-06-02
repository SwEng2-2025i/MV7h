from models.user import User # Importamos al usuario y revisamos en memoria
users_db = {} # Simulamos una memoria sin BD

def create_user(name, preferred_channel, available_channels):
    # Creación de usuario y prueba de errores
    if name in users_db:
        raise ValueError("Usuario ya existe.")
    if preferred_channel not in available_channels:
        raise ValueError("El canal preferido debe estar en los canales disponibles.")
    user = User(name, preferred_channel, available_channels)
    users_db[name] = user
    return user

def get_user(name):
    # Retorno de resultados guardados
    return users_db.get(name)
