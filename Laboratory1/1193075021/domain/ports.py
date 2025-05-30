from abc import ABC, abstractmethod
from domain.entities import User

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: pass

    @abstractmethod
    def find_by_name(self, name: str) -> User | None: pass

    @abstractmethod
    def list_all(self) -> list[User]: pass
