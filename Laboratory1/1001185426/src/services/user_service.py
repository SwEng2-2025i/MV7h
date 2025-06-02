from src.models import User

class UserService:
    def __init__(self):
        # Usaremos un diccionario en memoria: key = nombre, value = User
        self._users = {}

    def add_user(self, name: str, preferred: str, available: list[str]) -> User:
        if name in self._users:
            raise ValueError(f"El usuario '{name}' ya existe.")
        user = User(name, preferred, available)
        self._users[name] = user
        return user

    def get_all_users(self) -> list[User]:
        return list(self._users.values())

    def get_user_by_name(self, name: str) -> User:
        return self._users.get(name)
