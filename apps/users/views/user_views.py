from django.contrib.auth import get_user_model
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from core.views import CRUDSerializerClassBaseViewSet
from users.serializers import UserSerializer

User = get_user_model()


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    CRUDSerializerClassBaseViewSet
):
    queryset = User.objects.all()
    lookup_field = "username"

    retrieve_serializer = UserSerializer

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
