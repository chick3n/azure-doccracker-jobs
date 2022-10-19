import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.search import Search
from shared.models.job import Job

def main() -> None:    
    load_dotenv(find_dotenv())
    search = Search("km", "metadata_storage_path")
    texts = search.get_document_texts(['aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDgtMDJfQ2FuYWRhLnR4dA2', 
        'aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvdGhlc2F1cnVzLmpzb241', 
        'aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDgtMDFfUGFyaXMudHh00'])

    if len(texts) > 0:
        print('\n'.join(map(lambda text: text[0:100], texts)))
    else:
        print('no texts found.')



if __name__ == '__main__':
    main()