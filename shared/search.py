import os
import logging
from typing import List, Optional
from shared.models.job import Job, JobDocument
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class Search:
    def __init__(self, index):
        self.key = os.environ['Search_Key']
        self.endpoint = os.environ['Search_Endpoint']
        self.index = index

    def __get_search_client(self):
        return SearchClient(self.endpoint, self.index, AzureKeyCredential(self.key))

    def get_document_texts(self, documents:List[str], field:str='content') -> List[str]:
        texts = []
        for document_id in documents:
            document = self.get_document(document_id)
            if document and field in document:
                texts.append(document[field])

        return texts

    def get_document(self, record_id:str) -> Optional[str]:
        client = self.__get_search_client()
        return client.get_document(key=record_id)
        
