from rest_framework import mixins

from core.views import CRUDSerializerClassBaseViewSet
from tasks.models import Task
from tasks.serializers import CreateTaskSerializer, UpdateTaskSerializer
from tasks.services import TaskService


class TaskViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  CRUDSerializerClassBaseViewSet):
    queryset = Task.objects.all()

    create_serializer = CreateTaskSerializer
    update_serializer = UpdateTaskSerializer

    def perform_destroy(self, instance):
        TaskService(instance).delete_task()
