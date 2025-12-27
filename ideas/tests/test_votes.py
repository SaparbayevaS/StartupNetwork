import pytest
from rest_framework.test import APIClient
from core.models import CustomUser, Idea, Vote, Category

@pytest.fixture
def api_client():
    """
    Returns a DRF APIClient instance for making test requests
    """
    return APIClient()

@pytest.fixture
def user():
    """
    Creates and returns a test user
    """
    return CustomUser.objects.create_user(email="voter@example.com", password="password")

@pytest.fixture
def category():
    """
    Creates and returns a test category
    """
    return Category.objects.create(name="Tech")

@pytest.fixture
def idea(user, category):
    """
    Creates and returns a test idea
    """
    return Idea.objects.create(title="Idea1", description="Desc", author=user, category=category)

@pytest.mark.django_db
def test_create_vote(api_client, user, idea):
    """
    Test that a user can create a vote for an idea via the API
    """
    api_client.force_authenticate(user=user)
    data = {"idea": idea.id}
    
    response = api_client.post("/api/votes/", data, format='json')
    
   
    assert response.status_code == 201
    assert Vote.objects.filter(user=user, idea=idea).exists()