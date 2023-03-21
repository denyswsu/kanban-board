import pytest
from rest_framework.test import APIRequestFactory

from apps.users.models import User
from apps.users.views.api.user_views import UserViewSet


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore

        assert response.data == {
            "username": user.username,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
        }
