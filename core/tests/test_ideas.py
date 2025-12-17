import pytest
from rest_framework.test import APIClient
from core.models import CustomUser, Idea, Category

@pytest.fixture
def api_client():
    """Returns a DRF APIClient instance for making test requests
    """
    return APIClient()

@pytest.fixture
def user():
    """
    Creates and returns a test user
    """
    return CustomUser.objects.create_user(
        email="creator@example.com", password="password", full_name="Creator"
    )

@pytest.fixture
def category():
    """
    Creates and returns a test category
    """
    return Category.objects.create(name="Tech")

@pytest.mark.django_db
def test_create_idea(api_client, user, category):
    """
    Test that an authenticated user can create a new idea
    """
    api_client.force_authenticate(user=user)
    data = {
        "title": "New Idea",
        "description": "Awesome description",
        "category": category.id
    }
    response = api_client.post("/api/ideas/", data)
    
    assert response.status_code == 201
    assert Idea.objects.filter(title="New Idea").exists()

@pytest.mark.django_db
def test_list_ideas(api_client, user, category):
    """
    Test that the list of ideas returns all created ideas
    """
    Idea.objects.create(title="Idea1", description="Desc1", author=user, category=category)
    Idea.objects.create(title="Idea2", description="Desc2", author=user, category=category)
    
    response = api_client.get("/api/ideas/")
    
    assert response.status_code == 200
    assert len(response.data) == 2