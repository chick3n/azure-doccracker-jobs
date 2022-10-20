import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.queue import Queue

def main() -> None:    
    load_dotenv(find_dotenv())
    
    message = {
        'errors': [
            'Something went wrong.',
            'Cant solve this problem.',
            'Multiple error lines'
        ]
    }

    queue = Queue()
    error_queue = os.environ['Queue_ErrorName']
    queue.create(error_queue)
    print(f'create queue {error_queue}')
    
    queue.send(error_queue, json.dumps(message, indent=4, default=str))
    print(f'sent message to queue {error_queue}')

    messages = queue.peek('abstractive-summary')
    print(str(messages))

if __name__ == '__main__':
    main()