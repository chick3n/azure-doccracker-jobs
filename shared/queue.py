from typing import List
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy,
        QueueMessage
)

import os, uuid, base64

class Queue:
    def __init__(self):
        self.conn = os.environ['Queue_ConnectionString']
    
    def __client(self, queue_name:str):
        return QueueClient.from_connection_string(self.conn, queue_name #,
                            #message_encode_policy = BinaryBase64EncodePolicy(),
                            #message_decode_policy = BinaryBase64DecodePolicy()
                            )

    def create(self, queue_name:str):
        try:
            self.__client(queue_name).create_queue()
        except:
            pass

    def send(self, queue:str, message:str) -> None:
        #encoded_message = base64.b64encode(message.encode('utf8'))
        self.__client(queue).send_message(message)

    def peek(self, queue:str) -> List[QueueMessage]:
        return self.__client(queue).peek_messages(1)