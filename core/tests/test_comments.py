import pytest
from core.models import CustomUser, Idea, Comment, Category
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return CustomUser.objects.create_user("user@example.com", "password")

@pytest.fixture
def category():
    return Category.objects.create(name="Tech")

@pytest.fixture
def idea(user, category):
    return Idea.objects.create(title="Idea1", description="Desc", author=user, category=category)

@pytest.mark.django_db
def test_create_comment(api_client, user, idea):
    api_client.force_authenticate(user=user)
    data = {"content": "Nice idea!", "idea": idea.id}
    response = api_client.post("/api/comments/", data)
    assert response.status_code == 201
    assert Comment.objects.filter(content="Nice idea!").exists()