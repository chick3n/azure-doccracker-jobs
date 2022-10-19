from datetime import datetime
from typing import List, Type
from dataclasses import dataclass, field


class JobState:
    Pending = 'Pending'
    Completed = 'Completed'
    Failed = 'Failed'

@dataclass
class JobRequest:
    id: str
    index: str
    action: str

@dataclass
class JobDocument:
    id: str
    key: str
    title: str

    @classmethod
    def from_entity(cls, entity):
        return cls(entity.PartitionKey, entity.RowKey, entity.Title)

@dataclass
class Job:
    id: str
    index: str
    state: str
    action: str
    created_on: datetime = None
    documents: List[Type[JobDocument]] = field(default_factory=list)

    @classmethod
    def from_entity(cls, entity):
        job = cls(entity.RowKey, entity.PartitionKey, entity.State, entity.Action, entity.CreatedOn)
        for d in entity.Documents:
            job.documents.append(JobDocument.from_entity(d))
        return job


class DbEntity:
    PartitionKey: str
    RowKey: str
    Timestamp: datetime

class JobDocumentEntity(DbEntity):
    def __init__(self, table_entity:dict=None):
        if table_entity is not None:
            for k, v in table_entity.items():
                setattr(self, k, v)
    Title: str

class JobEntity(DbEntity):
    def __init__(self, table_entity:dict=None, document_entities:List[JobDocumentEntity]=None):
        if table_entity is not None:
            for k, v in table_entity.items():
                setattr(self, k, v)

        if document_entities is not None:
            self.Documents = document_entities

    PartitionKey: str
    RowKey: str
    State: str
    Action: str
    CreatedOn: datetime
    Documents: List[JobDocumentEntity] = field(default_factory=list)
