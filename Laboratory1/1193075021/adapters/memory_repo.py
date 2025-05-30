from domain.ports import UserRepository
from domain.entities import User

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User) -> None:
        self.users[user.name] = user

    def find_by_name(self, name: str) -> User | None:
        return self.users.get(name)

    def list_all(self) -> list[User]:
        return list(self.users.values())
