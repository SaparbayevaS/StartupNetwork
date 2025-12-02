from rest_framework import viewsets, permissions, filters, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Idea, Comment, Category, Vote
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
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


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshTokenAPIView(TokenRefreshView):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]


class IdeaViewSet(viewsets.ModelViewSet):
    queryset = Idea.objects.all()
    serializer_class = IdeaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        return Idea.objects.select_related('author', 'category').prefetch_related('comments', 'votes').filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Comment.objects.select_related('author', 'idea').filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Vote.objects.select_related("user", "idea").filter(deleted_at__isnull=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)