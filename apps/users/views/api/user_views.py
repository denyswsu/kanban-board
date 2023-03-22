from django.contrib.auth import get_user_model
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.views import CRUDSerializerClassBaseViewSet
from users.serializers import UserSerializer
from users.serializers.users_serializers import CreateUserSerializerCaseInsensitive

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


class RegisterUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    # authentication_classes = []

    serializer_class = CreateUserSerializerCaseInsensitive

