import os
import logging
from typing import List, Optional
from shared.models.job import Job, JobDocument
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class Search:
    def __init__(self, index, primary_key_name):
        self.key = os.environ['Search_Key']
        self.endpoint = os.environ['Search_Endpoint']
        self.primary_key_name = primary_key_name
        self.index = index

    def __get_search_client(self):
        return SearchClient(self.endpoint, self.index, AzureKeyCredential(self.key))

    def get_document_texts(self, documents:List[str]) -> List[str]:
        texts = []
        for document in documents:
            text = self.get_document_text(document)
            if text:
                texts.append(text)

        return texts

    def get_document_text(self, record_id:str) -> Optional[str]:
        client = self.__get_search_client()
        result = client.get_document(key=record_id)
        if result:
            return result['content']
        return None
        
