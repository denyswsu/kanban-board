from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.boards.models import Board
from apps.boards.serializers import BoardSerializer
from apps.core.views import CRUDSerializerClassBaseViewSet


class BoardsViewSet(ModelViewSet, CRUDSerializerClassBaseViewSet):
    permission_classes = (IsAuthenticated,)
    retrieve_serializer = BoardSerializer

    def get_queryset(self):
        return Board.objects.select_related("owner")
