import pytest
from rest_framework.test import APIClient
from core.models import CustomUser, Idea, Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        email="creator@example.com", password="password", full_name="Creator"
    )

@pytest.fixture
def category():
    return Category.objects.create(name="Tech")

@pytest.mark.django_db
def test_create_idea(api_client, user, category):
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
    Idea.objects.create(title="Idea1", description="Desc1", author=user, category=category)
    Idea.objects.create(title="Idea2", description="Desc2", author=user, category=category)
    response = api_client.get("/api/ideas/")
    assert response.status_code == 200
    assert len(response.data) == 2