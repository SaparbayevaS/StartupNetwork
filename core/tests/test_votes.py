import pytest
from core.models import CustomUser, Idea, Vote, Category
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return CustomUser.objects.create_user("voter@example.com", "password")

@pytest.fixture
def category():
    return Category.objects.create(name="Tech")

@pytest.fixture
def idea(user, category):
    return Idea.objects.create(title="Idea1", description="Desc", author=user, category=category)

@pytest.mark.django_db
def test_create_vote(api_client, user, idea):
    api_client.force_authenticate(user=user)
    data = {"idea": idea.id}
    response = api_client.post("/api/votes/", data, format='json')
    
    assert response.status_code == 201
    assert Vote.objects.filter(user=user, idea=idea).exists()