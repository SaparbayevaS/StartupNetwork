from typing import Any
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
)

class RegisterAPIView(CreateAPIView):
    """
    API view to register a new user.
    """
    serializer_class = RegisterSerializer


class LoginAPIView(TokenObtainPairView):
    """
    API view to log in a user and return JWT tokens.
    """
    serializer_class = LoginSerializer


class RefreshTokenAPIView(TokenRefreshView):
    """
    API view to refresh JWT access token.
    """
    pass
