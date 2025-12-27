from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    IdeaViewSet,
    CommentViewSet,
    VoteViewSet,
    RegisterAPIView,
    LoginAPIView,
    RefreshTokenAPIView
)

# ----------------------------
# Router для ViewSet-ов
# ----------------------------
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')  # Категории идей
router.register(r'ideas', IdeaViewSet, basename='idea')               # CRUD для идей
router.register(r'comments', CommentViewSet, basename='comment')      # CRUD для комментариев
router.register(r'votes', VoteViewSet, basename='vote')               # CRUD для голосов

# ----------------------------
# URL-шаблоны приложения ideas
# ----------------------------
urlpatterns = [
    # Подключение роутера с ViewSet-ами
    path('', include(router.urls)),
]
