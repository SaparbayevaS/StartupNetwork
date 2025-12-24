from typing import Optional, Any

from django.db.models import Model, BooleanField, DateTimeField, EmailField, CharField, TextField, OneToOneField, ImageField, CASCADE, ForeignKey, IntegerField, ManyToManyField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from .constants import (
    USER_FULL_NAME_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    IDEA_TITLE_MAX_LENGTH,
    PROFILE_DEFAULT_COUNT,
)


class AbstactSoftDeletableModel(Model):
    """
    Base model for soft delete.
    Contains created, updated, deleted time fields.
    """
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)
    
    def delete(self, using: str = None, keep_parents: bool = False) -> None:
        """
        Marks object as deleted by setting deleted_at time.
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
           
    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser model.
    Used to create users and superusers.
    """
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> 'CustomUser':
        """
        Created a user with email and password.
        """
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> 'CustomUser':
        """
        Created a superuser with admin permissions.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstactSoftDeletableModel):
    """
    Custom user mmodel.
    Uses email as login field.
    """
    email = EmailField(unique=True)
    full_name = CharField(max_length=USER_FULL_NAME_MAX_LENGTH, blank=True)
    bio = TextField(blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        return self.email
    

class UserProfile(Model):
    """
    User profile model.
    Connected to CustomUser with one-to-one relation.
    """
    user = OneToOneField(CustomUser, on_delete=CASCADE, related_name='profile')
    total_ideas = IntegerField(default=PROFILE_DEFAULT_COUNT)
    total_comments = IntegerField(default=PROFILE_DEFAULT_COUNT)
    total_votes = IntegerField(default=PROFILE_DEFAULT_COUNT)

    def __str__(self) -> str:
        return f"Profile of {self.user.email}"


class Category(AbstactSoftDeletableModel):
    """
    Category for ideas.
    """
    name = CharField(max_length=CATEGORY_NAME_MAX_LENGTH)

    def __str__(self) -> str:
        return self.name


class Idea(AbstactSoftDeletableModel):
    """
    Idea model.
    Contains title, description, category and author.
    """
    title = CharField(max_length=IDEA_TITLE_MAX_LENGTH)
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE, related_name='ideas')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='ideas')

    def __str__(self) -> str:
        return self.title


class Comment(AbstactSoftDeletableModel):
    """
    Comment model for ideas.
    """
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='comments')
    content = TextField()

    def __str__(self) -> str:
        return f"{self.author.email} on {self.idea.title}"


class Vote(AbstactSoftDeletableModel):
    """
    Vote model.
    ONe user can only vote for one idea.
    """
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='votes')
    user = ForeignKey(CustomUser, on_delete=CASCADE, related_name='votes')

    class Meta:
        unique_together = ('idea', 'user')

    def __str__(self) -> str:
        return f"{self.user.email} voted on {self.idea.title}"    