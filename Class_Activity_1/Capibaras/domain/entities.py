import uuid
from dataclasses import dataclass,field

@dataclass
class Task:
    title: str
    done: bool = False
    id: str= field(default_factory=lambda: str(uuid.uuid4()))

    def mark_done(self):
        self.done = True
