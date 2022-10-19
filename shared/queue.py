from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)

import os, uuid

class Queue:
    def __init__(self):
        self.conn = os.environ['Queue_ConnectionString']
    
    def __client(self, queue_name:str):
        return QueueClient.from_connection_string(self.conn, queue_name)

    def create(self, queue_name:str):
        try:
            self.__client(queue_name).create_queue()
        except:
            pass

    def send(self, queue:str, message:str) -> None:
        self.__client(queue).send_message(message)