from core.models import CustomUser, Idea, Comment, Category, Vote
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
    HTTP_401_UNAUTHORIZED,
)


class AuthTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="password123", full_name="TestUser"
        )

    def test_register_user(self):
        url = reverse("register")
        data = {"email": "new@example.com", "password": "pass1234", "full_name": "NewUser"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_register_existing_email(self):
        url = reverse("register")
        data = {"email": self.user.email, "password": "pass1234"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        url = reverse("login")
        data = {"email": self.user.email, "password": "password123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        url = reverse("login")
        data = {"email": self.user.email, "password": "wrongpassword123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class IdeaTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="ideauser@example.com", password="password123")
        self.category = Category.objects.create(name="TestCategory")
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_idea(self):
        url = reverse("idea-list")
        data = {"title": "MyIdea", "description": "IdeaDescription", "category": self.category.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "MyIdea")

    def test_create_idea_unauthenticated(self):
        self.client.credentials()
        url = reverse("idea-list")
        data = {"title": "NoAuth", "description": "Desc", "category": self.category.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_list_ideas(self):
        Idea.objects.create(title="Idea1", description="Desc", author=self.user, category=self.category)
        url = reverse("idea-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_other_idea_forbidden(self):
        other_user = CustomUser.objects.create_user(email="other@example.com", password="pass")
        idea = Idea.objects.create(title="Other", description="Desc", author=other_user, category=self.category)
        url = reverse("idea-detail", args=[idea.id])
        data = {"title": "Hacked", "description": "Desc", "category": self.category.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)


class CommentTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="comments@example.com", password="pass")
        self.category = Category.objects.create(name="Cat")
        self.idea = Idea.objects.create(title="Idea1", description="Desc", author=self.user, category=self.category)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_comment(self):
        url = reverse("comment-list")
        data = {"content": "Nice Idea!", "idea": self.idea.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "Nice Idea!")

    def test_create_comment_unauthenticated(self):
        self.client.credentials()
        url = reverse("comment-list")
        data = {"content": "Bad", "idea": self.idea.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class VoteTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="vote@example.com", password="password123")
        self.category = Category.objects.create(name="Cat")
        self.idea = Idea.objects.create(title="Idea1", description="Desc", author=self.user, category=self.category)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def test_create_vote(self):
        url = reverse("vote-list")
        data = {"idea": self.idea.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data["idea"], self.idea.id)

    def test_create_vote_unauthenticated(self):
        self.client.credentials()
        url = reverse("vote-list")
        data = {"idea": self.idea.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)