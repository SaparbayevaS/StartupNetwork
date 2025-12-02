
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

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'ideas', IdeaViewSet, basename='idea')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'votes', VoteViewSet, basename='vote')


urlpatterns = [
   
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('refresh/', RefreshTokenAPIView.as_view(), name='refresh-token'),

    path('', include(router.urls)),
]