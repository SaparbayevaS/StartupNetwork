from rest_framework import viewsets,permissions,filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Prefetch
from .models import Idea,Comment,Category,Vote
from .serializers import (
    IdeaSerializer,
    CommentSerializer,      
    CategorySerializer,
    VoteSerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
class IdeaViewSet(viewsets.ModelViewSet):
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]    
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        return (
            Idea.objects.select_related('author')
            .prefetch_related(
                "comments",
                "votes",
                "idea_categories__category"
            )
            .filter(is_deleted=False)
        )

class CommentViewSet(viewsets.ModelViewSet):
        serializer_class = CommentSerializer
        permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
        authentication_classes = [JWTAuthentication]
    
        def get_queryset(self):
            return (
                Comment.objects.select_related('author', 'idea')
                .filter(is_deleted=False)
            )
        def perform_create(self, serializer):
            serializer.save(author=self.request.user)

class VoteViewSet(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return (
        Vote.objects
        .select_related("user", "idea")
        .filter(is_deleted=False)
        )
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)