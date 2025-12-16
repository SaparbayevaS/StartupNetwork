import pytest
from rest_framework.test import APIClient
from core.models import CustomUser

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        "email": "user@example.com",
        "password": "strongpassword",
        "full_name": "Test User"
    }
    response = api_client.post("/api/auth/register/", data)
    assert response.status_code == 201
    assert CustomUser.objects.filter(email="user@example.com").exists()

@pytest.mark.django_db
def test_login_user(api_client):
    user = CustomUser.objects.create_user(
        email="user2@example.com",
        password="strongpassword",
        full_name="User Two"
    )
    data = {
        "email": "user2@example.com",
        "password": "strongpassword"
    }
    response = api_client.post("/api/auth/login/", data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data