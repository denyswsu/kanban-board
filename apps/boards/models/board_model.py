from django.db import models

from apps.core.models import TimeStampedModel


class Board(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey("users.User", related_name="boards", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
