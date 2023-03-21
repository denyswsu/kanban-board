from rest_framework import serializers

from boards.models import Column
from tasks.serializers import TaskSerializer


class ColumnSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Column
        fields = ("id", "name", "board", "order", "tasks")
