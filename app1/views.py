from django.shortcuts import render
import requests
# Create your views here.
from celery.worker.control import control_command
from celery.worker.control import inspect_command

from django.http import HttpResponse
from concurrent.futures.thread import ThreadPoolExecutor
from .tasks import add


def add_with_priority( x, y, priority ):
    """add_with_priority

    """
    res = add.apply_async(args=[x, y, priority], routing_key='tasks', priority=priority)
    if res.ready():
        print("Result from {} + {} with priority {} is {}".format(x, y, priority, res))


def test_task(request):
    """test_task
    """
    test_samples = [[4, 5, 1], [2, 9, 2], [10, 25, 3], [4, 5, 4], [4, 5, 5], [4, 5, 6], [4, 5, 7], [4, 5, 8]]

    with ThreadPoolExecutor(max_workers=4) as e:
        for test in test_samples:
            e.submit(add_with_priority, *test)

    return HttpResponse("task running...")


@control_command(
    args=[('n', int)],
    signature='[N=1]',  # <- used for help on the command-line.
)
def increase_prefetch_count(state, n=1):
    # celery -A celery_test control increase_prefetch_count 3

    state.consumer.qos.increment_eventually(n)
    return {'ok': 'prefetch count incremented'}


@inspect_command()
def current_prefetch_count(state):
    # celery -A celery_test inspect current_prefetch_count
    
    return {'prefetch_count': state.consumer.qos.value}
