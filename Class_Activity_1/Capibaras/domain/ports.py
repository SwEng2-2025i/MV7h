from abc import ABC, abstractmethod
from .entities import Task

# Puerto de entrada
class TaskInputPort(ABC):
    @abstractmethod
    def create_task(self, title: str) -> Task: pass

    @abstractmethod
    def get_all_tasks(self) -> list[Task]: pass

    @abstractmethod
    def mark_task(self,id:str)->bool:pass

# Puerto de salida
class TaskOutputPort(ABC):
    @abstractmethod
    def save(self, task: Task) -> None: pass

    @abstractmethod
    def list_all(self) -> list[Task]: pass

    @abstractmethod
    def get_by_id(self,id)->Task:pass
