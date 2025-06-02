from abc import ABC, abstractmethod
from .entities import Task

# Puerto de entrada
class TaskInputPort(ABC):
    @abstractmethod
    def create_task(self, title: str) -> Task: pass

    @abstractmethod
    def get_all_tasks(self) -> list[Task]: pass

    @abstractmethod
    def marked_as_complete(self, task_id: str) -> Task: pass 

# Puerto de salida
class TaskOutputPort(ABC):
    @abstractmethod
    def save(self, task: Task) -> None: pass

    @abstractmethod
    def list_all(self) -> list[Task]: pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task:pass
