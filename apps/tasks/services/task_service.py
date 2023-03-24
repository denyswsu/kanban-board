from django.db import transaction
from django.db.models import F

from boards.models import Column
from tasks.models import Task


class TaskService:
    """Board Tasks manipulations"""
    def __init__(self, task: Task):
        self.task = task
        self.current_order = task.order

    @transaction.atomic
    def move_task(self, new_order: int, column: Column, **kwargs):
        """Move task within column or to another column, and shift tasks accordingly"""
        if self.task.column == column:
            self.move_task_in_column(new_order)
        else:
            self.move_task_to_column(new_order, column)

        if kwargs.get("save", False):
            self.task.save()

    def move_task_in_column(self, new_order: int):
        if new_order > self.current_order:
            self.move_down(new_order)
        else:
            self.move_up(new_order)

    def move_down(self, new_order: int):
        self.task.column.tasks.filter(
            order__gt=self.current_order, order__lte=new_order
        ).update(order=F("order") - 1)
        self.task.order = new_order

    def move_up(self, new_order: int):
        self.task.column.tasks.filter(
            order__gte=new_order, order__lt=self.current_order
        ).update(order=F("order") + 1)
        self.task.order = new_order

    def move_task_to_column(self, new_order: int, new_column: Column):
        # remove task from current column
        self.task.column.tasks.filter(
            order__gt=self.current_order
        ).update(order=F("order") - 1)
        # insert task to new column
        new_column.tasks.filter(
            order__gte=new_order
        ).update(order=F("order") + 1)
        self.task.column = new_column
        self.task.order = new_order

    @transaction.atomic
    def delete_task(self):
        """Delete column and shift other columns accordingly"""
        self.task.column.tasks.filter(
            order__gt=self.current_order
        ).update(order=F("order") - 1)
        self.task.delete()
