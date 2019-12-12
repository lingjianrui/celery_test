from kombu import Exchange, Queue

CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_QUEUES = (
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
    Queue('highs', routing_key='highs', consumer_arguments={'x-priority': 5}, queue_arguments={'x-max-priority': 10}),
    Queue('high', routing_key='high', consumer_arguments={'x-priority': 5}),
    Queue('low', routing_key='low',consumer_arguments={'x-priority': 1}),
)
