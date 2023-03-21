from django.db import models

from core.models import TimeStampedModel


class Task(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey("users.User", related_name="tasks", on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey("users.User", related_name="assigned_tasks", on_delete=models.SET_NULL, null=True)
    column = models.ForeignKey("boards.Column", related_name="tasks", on_delete=models.CASCADE)
    board = models.ForeignKey("boards.Board", related_name="tasks", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    # TODO:
    # labels
    # comments
    # attachments

    class Meta:
        ordering = ("order",)
        unique_together = ("column", "order")

    def __str__(self):
        return f"{self.board.name} - {self.column.name} - {self.name}"
