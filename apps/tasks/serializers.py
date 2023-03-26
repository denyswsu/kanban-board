from datetime import datetime

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
        validated_data["order"] = column.get_new_task_order()
        task = Task.objects.create(**validated_data)
        if assigned_to := validated_data.get("assigned_to"):
            TaskService(task).notify_task_assigned(assigned_to, self.context["request"].user)
        return task


class UpdateTaskSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(required=False)

    class Meta:
        model = Task
        fields = ("id", "name", "column", "order", "description", "assigned_to", "deadline")
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

    def validate_deadline(self, deadline: datetime):
        if deadline < datetime.utcnow():
            raise serializers.ValidationError("Deadline cannot be in the past.")

        self.instance.is_expired = False
        return deadline

    @transaction.atomic
    def update(self, task, validated_data):
        user = self.context["request"].user
        column = validated_data.pop("column", task.column)
        if "order" in validated_data:
            TaskService(task).move_task(validated_data.pop("order"), column)

        if "assigned_to" in validated_data and validated_data["assigned_to"] != task.assigned_to:
            TaskService(task).notify_task_assigned(validated_data["assigned_to"], user)
        else:
            updated_fields = {f: v for f, v in validated_data.items() if v != getattr(task, f)}
            TaskService(task).notify_task_updated(updated_fields, user)

        super().update(task, validated_data)
        return task
