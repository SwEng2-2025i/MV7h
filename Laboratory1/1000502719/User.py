from dataclasses import dataclass,field
import uuid

@dataclass
class User:
    name: str
    preferred_channel: str
    available_channels: list
    notifAttempts: list
    id:str=field(default_factory=lambda: str(uuid.uuid4()))
    