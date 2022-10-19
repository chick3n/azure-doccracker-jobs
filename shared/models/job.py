from datetime import datetime
from typing import List, Type
from dataclasses import dataclass, field

@dataclass
class JobDocument:
    id: str
    key: str
    title: str

@dataclass
class JobRequest:
    id: str
    index_config: str
    action: str

@dataclass
class Job:
    id: str
    index_name: str
    state: str
    action: str
    created_on: datetime = None
    documents: List[Type[JobDocument]] = field(default_factory=list)
