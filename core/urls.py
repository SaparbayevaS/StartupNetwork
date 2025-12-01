from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, IdeaViewSet, CommentViewSet, VoteViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'ideas', IdeaViewSet, basename='idea') 
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = router.urls

