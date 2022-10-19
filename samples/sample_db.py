import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.database import Database

def main() -> None:    
    load_dotenv(find_dotenv())
    database = Database()
    job = database.get_job('ukraine-invasion', '08c008a1-73e1-4e69-ace2-1829dd5aff15')
    print(json.dumps(vars(job), indent=4, default=str))

if __name__ == '__main__':
    main()