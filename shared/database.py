import os
from typing import Type
from shared.models.job import Job, JobDocument
from azure.data.tables import TableClient
from azure.core.exceptions import HttpResponseError

class Database:
    def __init__(self):
        self.conn = os.environ['Database_ConnectionString']
        self.table_job = 'jobs'
        self.table_job_documents = 'jobDocuments'

    def get_job(self, p_key, row_key):
        with TableClient.from_connection_string(self.conn, self.table_job) as table_client:
            try:
                parameters = {"pkey": p_key, "rkey": row_key}
                name_filter = "PartitionKey eq @pkey and RowKey eq @rkey"
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=["PartitionKey", "RowKey", "State", "Action", "CreatedOn"], parameters=parameters
                )

                for entity in queried_entities:
                    return Job(row_key, p_key, entity['Action'], entity['State'], entity['CreatedOn'],
                        self.get_job_documents(row_key))
                    
            except HttpResponseError as e:
                return None

        return None
        
    def get_job_documents(self, p_key):
        documents:List[Type[JobDocument]] = []
        with TableClient.from_connection_string(self.conn, self.table_job_documents) as table_client:
            try:
                parameters = {"pkey": p_key}
                name_filter = "PartitionKey eq @pkey"
                queried_entities = table_client.query_entities(
                    query_filter=name_filter, select=["PartitionKey", "RowKey", "Title"], parameters=parameters
                )

                for entity in queried_entities:
                    documents.append(JobDocument(entity['PartitionKey'], entity['RowKey'], entity['Title']))

            except HttpResponseError as e:
                print(e.message)

            return documents