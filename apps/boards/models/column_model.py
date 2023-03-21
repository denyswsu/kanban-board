from django.db import models

from apps.core.models import TimeStampedModel


class Column(TimeStampedModel):
    name = models.CharField(max_length=55)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    board = models.ForeignKey("boards.Board", related_name="columns", on_delete=models.CASCADE)

    class Meta:
        ordering = ("order",)
        unique_together = ("board", "order")

    def __str__(self):
        return f"{self.board.name} - {self.name}"

    def next_board_order(self):
        return self.board.columns.count()
