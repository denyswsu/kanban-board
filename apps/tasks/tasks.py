from datetime import datetime

from config import celery_app
from tasks.models import Task
from tasks.services import TaskService


@celery_app.task()
def expire_tasks():
    tasks = Task.objects.filter(deadline__lt=datetime.utcnow(), is_expired=False)
    tasks.update(is_expired=True)
    [TaskService(task).notify_task_expired() for task in tasks]
    return tasks.count()
