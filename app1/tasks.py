
from __future__ import absolute_import
from celery import Celery
import sys
import time
from kombu import Queue, Exchange

# Create your tasks here
from celery import shared_task
import time

# Default settings-->
 
celery_app = Celery("priority_queue")

celeryconfig = {}
celeryconfig['BROKER_URL'] = 'amqp://guest:**@localhost:5672//' 
celeryconfig['CELERY_QUEUES'] = (
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
)
celeryconfig['CELERY_ACKS_LATE'] = True
celeryconfig['CELERYD_PREFETCH_MULTIPLIER'] = 1

celery_app.config_from_object(celeryconfig)


@shared_task
def task1():
    time.sleep(3)
    return "completed"

@shared_task
def run_in_evry_15_sec(time_data):
    
    time.sleep(60)
    
    return "testing message"+str(time_data)


@celery_app.task(queue='tasks', ignore_result=True)
def add(x, y, priority):
    print("Adding {} and {} with priority {}".format(x, y, priority))
    time.sleep(5)
    print("Result {} and {} with priority {}".format(x, y, priority))
    return x + y


@celery_app.task(queue='tasks', ignore_result=True)
def add_new(x, y, priority):
    print("Adding {} and {} with priority {}".format(x, y, priority))
    time.sleep(5)
    print("Result {} and {} with priority {}".format(x, y, priority))
    return x + y + x