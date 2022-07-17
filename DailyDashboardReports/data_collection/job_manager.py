import os, sys


class JobManager(object):
    jobs = []


#  TODO: add support for multiprocessing, exception handling if applicable
def execute_job_queue():
    for job, args_ in JobManager.jobs:
        job(*args_)