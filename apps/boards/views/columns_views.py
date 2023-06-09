from rest_framework import mixins

from boards.models import Column
from boards.serializers import UpdateColumnSerializer, CreateColumnSerializer
from boards.services.column_service import ColumnService
from core.views import CRUDSerializerClassBaseViewSet


class ColumnsViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     CRUDSerializerClassBaseViewSet):
    queryset = Column.objects.all()

    create_serializer = CreateColumnSerializer
    update_serializer = UpdateColumnSerializer

    def perform_destroy(self, instance):
        ColumnService(instance).delete_column()
