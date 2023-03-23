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
        # unique_together = ("board", "order")
        constraints = [
            UniqueConstraint(
                name='unique_columns_order',
                fields=("board", "order"),
                deferrable=Deferrable.DEFERRED,
            )
        ]

    def __str__(self):
        return f"{self.board.name} - {self.name}"
