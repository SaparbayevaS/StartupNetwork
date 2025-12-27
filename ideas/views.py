from typing import Any
from django.utils import timezone
from rest_framework.filters import SearchFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.authentication import JWTAuthentication

from ideas.models import Idea, Comment, Vote, Category
from .serializers import (
    IdeaSerializer,
    CommentSerializer,
    CategorySerializer,
    VoteSerializer
)

class IsAuthorOrReadOnly(BasePermission):
    """
    Permission to allow only authors of an object to edit it.
    Read-only access is allowed to all users.
    """
    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "author", None) == request.user


class CategoryViewSet(ViewSet):
    """
    ViewSet to manage categories: list, retrieve, create, update, delete.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def list(self, request: Request) -> Response:
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int | None = None) -> Response:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk: int | None = None) -> Response:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: int | None = None) -> Response:
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"detail": "Not found."}, status=HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)
