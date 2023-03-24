import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("kanban_board")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

TASK_SERIALIZER = 'json'
ACCEPT_CONTENT = ['json']


app.conf.update(
    BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND='django-db',
    CELERY_TIMEZONE=settings.TIME_ZONE,
    CELERYBEAT_SCHEDULE={
        "expire_tasks": {
            "task": "tasks.tasks.expire_tasks",
            "schedule": crontab(),  # once per minute
            "args": ()
        },
    },
)
