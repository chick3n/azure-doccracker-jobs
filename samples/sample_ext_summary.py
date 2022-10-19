import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.search import Search
from shared.models.job import Job
from shared.extractive_summary import ExtractiveSummary

def main() -> None:    
    load_dotenv(find_dotenv())
    search = Search("km")
    texts = search.get_document_texts(['aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDgtMDJfQ2FuYWRhLnR4dA2', 
        'aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvdGhlc2F1cnVzLmpzb241', 
        'aHR0cHM6Ly9zdGdkZW1vZG9jdW1lbnRzLmJsb2IuY29yZS53aW5kb3dzLm5ldC9kb2N1bWVudHMvMjAyMi0tMDgtMDFfUGFyaXMudHh00'])

    extsum = ExtractiveSummary(texts, summary_sentence_length=10)
    summary, errors = extsum.summarize()

    if errors:
        print('errors', errors)
    else: print('summary', summary)

if __name__ == '__main__':
    main()