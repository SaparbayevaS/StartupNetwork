from rest_framework.filters import SearchFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils import timezone
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Idea, Comment, Category, Vote
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    IdeaSerializer,
    CommentSerializer,
    CategorySerializer,
    VoteSerializer
)

# ----------------------------
# Auth Views
# ----------------------------
class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshTokenAPIView(TokenRefreshView):
    pass

# ----------------------------
# Category
# ----------------------------
class CategoryViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)

# ----------------------------
# Idea
# ----------------------------
class IdeaViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']

    def list(self, request):
        queryset = Idea.objects.select_related('author', 'category').prefetch_related('comments', 'votes').filter(deleted_at__isnull=True)
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)
        serializer = IdeaSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            idea = Idea.objects.select_related('author', 'category').prefetch_related('comments', 'votes').get(pk=pk, deleted_at__isnull=True)
        except Idea.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = IdeaSerializer(idea)
        return Response(serializer.data)

    def create(self, request):
        serializer = IdeaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            idea = Idea.objects.get(pk=pk, deleted_at__isnull=True)
        except Idea.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, idea)
        serializer = IdeaSerializer(idea, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            idea = Idea.objects.get(pk=pk, deleted_at__isnull=True)
        except Idea.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, idea)
        idea.deleted_at = timezone.now()
        idea.save()
        return Response(status=HTTP_204_NO_CONTENT)

# ----------------------------
# Comment
# ----------------------------
class CommentViewSet(ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Comment.objects.select_related('author', 'idea').filter(deleted_at__isnull=True)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            comment = Comment.objects.select_related('author', 'idea').get(pk=pk, deleted_at__isnull=True)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def create(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk, deleted_at__isnull=True)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            comment = Comment.objects.get(pk=pk, deleted_at__isnull=True)
        except Comment.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, comment)
        comment.deleted_at = timezone.now()
        comment.save()
        return Response(status=HTTP_204_NO_CONTENT)

# ----------------------------
# Vote
# ----------------------------
class VoteViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Vote.objects.select_related("user", "idea").filter(deleted_at__isnull=True)
        serializer = VoteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            vote = Vote.objects.select_related("user", "idea").get(pk=pk, deleted_at__isnull=True)
        except Vote.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = VoteSerializer(vote)
        return Response(serializer.data)

    def create(self, request):
        serializer = VoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            vote = Vote.objects.get(pk=pk, deleted_at__isnull=True)
        except Vote.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = VoteSerializer(vote, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            vote = Vote.objects.get(pk=pk, deleted_at__isnull=True)
        except Vote.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        vote.deleted_at = timezone.now()
        vote.save()
        return Response(status=HTTP_204_NO_CONTENT)