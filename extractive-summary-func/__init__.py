import logging
import json
from sre_parse import State
import azure.functions as func
from shared.database import Database
from shared.extractive_summary import ExtractiveSummary
from shared.queue import Queue
from shared.search import Search
from shared.models.job import JobRequest, JobState, Job
import os

def main(msg: func.QueueMessage) -> None:
    queue_message = msg.get_body().decode('utf-8')
    #queue_message = '{"expirationTime":"2022-10-27T01:47:13.8666328+00:00","id":"8279b244-b2c7-4fe8-8846-0f0aaf71b6f9","index":"km","action":"ExtractiveSummary"}'
    try:
        json_request = json.loads(queue_message)
    except Exception as e:
        logging.exception(e)
        handle_failure(JobRequest(None, None, 'Unknown'), { 'errors': [str(e)], 'original': queue_message })
        return

    job_request = JobRequest(json_request['id'], json_request['index'], json_request['action'])
    if job_request.action != 'ExtractiveSummary':
        handle_failure(job_request, { 'errors': ['invalid action {} in queue id {}'.format(json_request['action'], msg.id)] })
        return
    
    try:
        handle_request(job_request)
    except Exception as e:
        logging.exception(e)
        handle_failure(job_request, { 'errors': [str(e)] })

def handle_request(job_request: JobRequest) -> None:
    database = Database()
    jobEntity = database.get_job(job_request.index, job_request.id)
    if jobEntity is None:
        raise Exception('database record PartitionKey: {} RowKey: {} not found.'.format(job_request.index, job_request.id))

    job = Job.from_entity(jobEntity)
    if job.state != JobState.Pending:
        logging.info('database record PartitionKey: {} RowKey: {} already handled.'.format(job_request.index, job_request.id))
        return
    elif len(job.documents) == 0:
        logging.info('database record PartitionKey: {} RowKey: {} has no documents.'.format(job_request.index, job_request.id))
        database.update_job_state(job.index, job.id, JobState.Completed)
        return

    search = Search(job_request.index)    
    texts = search.get_document_texts([document.key for document in job.documents])
    extractive_summary = ExtractiveSummary(texts)
    summary, errors = extractive_summary.summarize()

    if errors:
        database.update_job_state(job.index, job.id, JobState.Failed)
        handle_failure(job_request, { 'errors': errors })
        return

    handle_complete(job, summary)

def handle_complete(job: Job, summary: str) -> None:
    from shared.blobstorage import BlobStorage

    database = Database()
    database.update_job_state(job.index, job.id, JobState.Completed)

    storage = BlobStorage()
    storage.upload(os.environ['Storage_JobContainerName'], f'{job.index}_{job.id}.txt', summary)

def handle_failure(job_request: JobRequest, extra:dict = None) -> None:    
    error_queue = os.environ['Queue_ErrorName']
    error_request = vars(job_request)
    if(extra is not None):
        error_request = {**error_request, **extra}
    
    queue = Queue()
    queue.create(error_queue)
    queue.send(error_queue, json.dumps(error_request, indent=4, default=str))
