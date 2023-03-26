from django.db import transaction
from rest_framework import serializers

from boards.models import Column
from boards.services import ColumnService
from tasks.serializers import TaskSerializer


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Column
        fields = ("id", "name", "order", "tasks", "description")
        read_only_fields = ("id", "tasks")


class UpdateColumnSerializer(ColumnSerializer):
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Column
        fields = ("id", "name", "board", "order", "tasks", "description", "is_completed_column")
        read_only_fields = ("id", "board", "tasks")

    def validate_order(self, order):
        last_column_order = self.instance.board.get_last_column_order() or 0
        if order > last_column_order:
            order = last_column_order
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        if "order" in validated_data:
            order = validated_data.pop("order")
            ColumnService(instance).move_column(order)
        super().update(instance, validated_data)
        return instance


class CreateColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, required=False)

    class Meta:
        model = Column
        fields = ("id", "name", "board", "tasks", "description", "is_completed_column")
        read_only_fields = ("id", "order", "tasks")

    def create(self, validated_data):
        board = validated_data["board"]
        validated_data["order"] = board.get_new_column_order()
        column = Column.objects.create(**validated_data)
        return column
