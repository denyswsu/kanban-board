from django.urls import path, include

from apps.api.api_routers import router

# app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
]
