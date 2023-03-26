from django.db import models
from django.db.models import Deferrable, UniqueConstraint

from core.models import TimeStampedModel
from tasks.services import TaskService


class Task(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey("users.User", related_name="tasks", on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey("users.User", related_name="assigned_tasks", on_delete=models.SET_NULL, null=True)
    column = models.ForeignKey("boards.Column", related_name="tasks", on_delete=models.CASCADE)
    board = models.ForeignKey("boards.Board", related_name="tasks", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    # TODO: labels, comments, attachments

    class Meta:
        ordering = ("order",)
        constraints = [
            UniqueConstraint(
                name='unique_tasks_order',
                fields=("column", "order"),
                deferrable=Deferrable.DEFERRED,
            )
        ]

    def __str__(self):
        return f"{self.board.name} - {self.column.name} - {self.name}"

    def save(self, *args, **kwargs):
        self.board = self.column.board
        self.set_is_expired()
        self.notify_if_task_completed()
        super().save(*args, **kwargs)

    def set_is_expired(self):
        if self.deadline and self.deadline < self.created_at:
            self.is_expired = True

    def notify_if_task_completed(self):
        if self.completed or self.column.is_completed_column:
            TaskService(self).notify_task_completed()

    def users_to_notify(self, additional_users: list = None):
        users = [self.assigned_to, self.owner]
        if additional_users:
            users += additional_users
        return users
