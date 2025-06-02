# storage.py

from models.user import User

users = {    "Marco Perez": User(
        name="Marco Perez",
        preferred_channel="email",
        available_channels=["email", "sms"]
    )}

def add_user(user_data):
    user = User(**user_data)
    users[user.name] = user
    return f"{user.name} fue creado exitosamente"

def get_user(name):
    return users.get(name)

def list_users():
    return list(users.values())
