from rest_framework import serializers

from tasks.models import Task
from users.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer()

    class Meta:
        model = Task
        exclude = ("board", "column")
