from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F

from boards.models import Column
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from tasks.models import Task

User = get_user_model()


class TaskService:
    """Board Tasks manipulations"""
    def __init__(self, task: "Task"):
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

    # TODO: smart notify not only assigned_to but also owner/members(todo)
    def notify_task_assigned(self, assigned_to: User, assigned_by: User):
        if assigned_to:
            # TODO
            print(f"Notify {self.task.users_to_notify([assigned_to])} that {assigned_by} assigned {self.task} to him")

    def notify_task_updated(self, updated_fields: dict, updated_by: User):
        if updated_fields:
            # TODO
            print(f"Notify {self.task.users_to_notify()} that task {self.task} was updated by {updated_by}: {updated_fields}")

    def notify_task_completed(self):
        # TODO
        print(f"Notify {self.task.users_to_notify()} that task {self.task} was completed\n\n\n\n\n\n\n\n")
