from datetime import datetime

class JobEntity():
    PartitionKey: str
    RowKey: str
    State: str
    Action: str
    CreatedOn: datetime