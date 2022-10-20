import logging
import json
import sys
import os
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.database import Database
from shared.models.job import Job, JobEntity, JobState

def main() -> None:    
    load_dotenv(find_dotenv())
    database = Database()
    get_sample_job(database)
    update_state(database)

def get_sample_entity(database: Database) -> JobEntity:
    return database.get_job('km', '8279b244-b2c7-4fe8-8846-0f0aaf71b6f9')
    
def get_sample_job(database: Database) -> Job:    
    print('\n\nget_sample_job')
    job_entity = get_sample_entity(database)
    print(vars(job_entity))
    return Job.from_entity(job_entity)

def update_state(database: Database):
    print('\n\nupdate_state')
    job = Job.from_entity(get_sample_entity(database))
    entity = database.update_job_state(job.index, job.id, JobState.Completed)
    print(f'updated {entity.PartitionKey}/{entity.RowKey} state to {entity.State}')
    print(f'update state back to {job.state}')
    entity = database.update_job_state(job.index, job.id, job.state)
    print(f'updated {entity.PartitionKey}/{entity.RowKey} state to {entity.State}')


if __name__ == '__main__':
    main()