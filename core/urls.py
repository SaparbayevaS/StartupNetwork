from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh-token"),
]
