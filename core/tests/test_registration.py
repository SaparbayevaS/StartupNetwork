import pytest
from rest_framework.test import APIClient
from core.models import CustomUser

@pytest.fixture
def api_client():
    """
    Returns a DRF APIClient instance for making test requests
    """
    return APIClient()

@pytest.mark.django_db
def test_register_user(api_client):
    """
    Test that a user can successfully register via the AP
    """
    data = {
        "email": "user@example.com",
        "password": "strongpassword",
        "full_name": "Test User"
    }
    response = api_client.post("/api/register/", data)
    
    assert response.status_code == 201
    assert CustomUser.objects.filter(email="user@example.com").exists()

@pytest.mark.django_db
def test_login_user(api_client):
    """
    Test that a registered user can log in and receive JWT tokens
    """
    user = CustomUser.objects.create_user(
        email="user2@example.com",
        password="strongpassword",
        full_name="User Two"
    )
    data = {
        "email": "user2@example.com",
        "password": "strongpassword"
    }
    response = api_client.post("/api/login/", data)
    
    assert response.status_code == 200
    
    assert "access" in response.data
    assert "refresh" in response.data