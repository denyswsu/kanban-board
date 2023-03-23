from django.db import transaction
from django.db.models import F

from boards.models import Column


class ColumnService:
    """Board Columns manipulations"""
    def __init__(self, column: Column):
        self.column = column
        self.current_order = column.order

    def move_column(self, new_order: int, **kwargs):
        """Move column to new order and shift other columns accordingly"""
        if new_order > self.current_order:
            self.move_forward(new_order)
        else:
            self.move_backward(new_order)

        if kwargs.get("save", False):
            self.column.save()

    @transaction.atomic
    def move_forward(self, new_order: int):
        self.column.board.columns.filter(
            order__gt=self.current_order, order__lte=new_order
        ).update(order=F("order") - 1)
        self.column.order = new_order

    @transaction.atomic
    def move_backward(self, new_order: int):
        self.column.board.columns.filter(
            order__gte=new_order, order__lt=self.current_order
        ).update(order=F("order") + 1)
        self.column.order = new_order

    @transaction.atomic
    def delete_column(self):
        """Delete column and shift other columns accordingly"""
        self.column.board.columns.filter(
            order__gt=self.current_order
        ).update(order=F("order") - 1)
        self.column.delete()
