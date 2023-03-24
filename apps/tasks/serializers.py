from django.db import transaction
from rest_framework import serializers

from tasks.services import TaskService
from tasks.models import Task
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()

    class Meta:
        model = Task
        exclude = ("board", "column", "owner")


class CreateTaskSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assigned_to = UserSerializer(required=False)

    class Meta:
        model = Task
        fields = ("id", "name", "description", "assigned_to", "column", "owner")
        read_only_fields = ("id", "owner")

    def create(self, validated_data):
        column = validated_data["column"]
        validated_data["board"] = column.board
        validated_data["order"] = column.get_new_task_order()
        return Task.objects.create(**validated_data)


class UpdateTaskSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ("id", "name", "column", "order", "description", "assigned_to")
        read_only_fields = ("id",)

    def validate(self, data):
        self._validate_order(data)
        return data

    def _validate_order(self, data):
        order = data.get("order")
        if not order:
            return

        column = data.get("column", self.instance.column)
        new_task_order = column.get_new_task_order()
        if order > new_task_order:
            data["order"] = new_task_order

    @transaction.atomic
    def update(self, instance, validated_data):
        if "order" in validated_data:
            order = validated_data.pop("order")
            column = validated_data.pop("column", instance.column)
            TaskService(instance).move_task(order, column)
        super().update(instance, validated_data)
        return instance
