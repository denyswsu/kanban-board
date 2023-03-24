from django.db import models
from django.db.models import UniqueConstraint, Deferrable

from core.models import TimeStampedModel


class Column(TimeStampedModel):
    name = models.CharField(max_length=55, blank=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    board = models.ForeignKey("boards.Board", related_name="columns", on_delete=models.CASCADE)

    class Meta:
        ordering = ("order",)
        constraints = [
            UniqueConstraint(
                name='unique_columns_order',
                fields=("board", "order"),
                deferrable=Deferrable.DEFERRED,
            )
        ]

    def __str__(self):
        return f"{self.board.name} - {self.name}"

    def get_new_task_order(self):
        last_task_order = self.get_last_task_order()
        return last_task_order + 1 if last_task_order is not None else 0

    def get_last_task_order(self):
        last_task = self.tasks.last()
        return last_task.order if last_task else None
