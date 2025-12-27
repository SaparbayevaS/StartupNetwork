from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPIView,
    LoginAPIView,
    RefreshTokenAPIView
)

# ----------------------------
# URL-шаблоны для пользователей
# ----------------------------
urlpatterns = [
    # Регистрация нового пользователя
    path('register/', RegisterAPIView.as_view(), name='register'),

    # Вход пользователя и выдача JWT токенов
    path('login/', LoginAPIView.as_view(), name='login'),

    # Обновление access токена
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh-token'),
]
