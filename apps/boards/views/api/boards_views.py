from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from boards.models import Board, Column
from boards.serializers import BoardSerializer
from core.views import CRUDSerializerClassBaseViewSet
from tasks.models import Task


class BoardsViewSet(ModelViewSet, CRUDSerializerClassBaseViewSet):
    permission_classes = (IsAuthenticated,)
    retrieve_serializer = BoardSerializer

    def get_queryset(self):
        return Board.objects.select_related("owner").prefetch_related(
            Prefetch("columns", queryset=Column.objects.prefetch_related(
                Prefetch("tasks", queryset=Task.objects.select_related("assigned_to", "owner"))
            ))
        )
