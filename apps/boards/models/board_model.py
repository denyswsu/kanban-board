from django.db import models

from core.models import TimeStampedModel


class Board(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey("users.User", related_name="boards", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_new_column_order(self):
        last_column_order = self.get_last_column_order()
        return last_column_order + 1 if last_column_order else 0

    def get_last_column_order(self):
        last_column = self.columns.last()
        return last_column.order if last_column else None
