from django.db import models, transaction
from django.db.models import UniqueConstraint, Deferrable

from core.models import TimeStampedModel


class Column(TimeStampedModel):
    name = models.CharField(max_length=55, blank=False)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    board = models.ForeignKey("boards.Board", related_name="columns", on_delete=models.CASCADE)
    is_completed_column = models.BooleanField(null=True, default=None, unique=True)

    class Meta:
        ordering = ("order",)
        constraints = [
            UniqueConstraint(
                name="unique_columns_order",
                fields=("board", "order"),
                deferrable=Deferrable.DEFERRED,
            ),
            UniqueConstraint(
                name="unique_completed_column",
                fields=("is_completed_column", "board"),
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

    def save(self, *args, **kwargs):
        self.make_completed_column_unique()
        super().save(*args, **kwargs)

    def make_completed_column_unique(self):
        if self.is_completed_column is False:
            self.is_completed_column = None
        if self.is_completed_column:
            self.board.columns.filter(is_completed_column=True).update(is_completed_column=None)