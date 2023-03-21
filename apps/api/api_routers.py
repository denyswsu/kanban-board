from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from boards.views.api.boards_views import BoardsViewSet
from users.views.api.user_views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("boards", BoardsViewSet, basename="boards")
