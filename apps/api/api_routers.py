from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from boards.views import BoardsViewSet, ColumnsViewSet
from tasks.views import TaskViewSet
from users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("boards", BoardsViewSet, basename="boards")
router.register("columns", ColumnsViewSet, basename="columns")
router.register("tasks", TaskViewSet, basename="tasks")
