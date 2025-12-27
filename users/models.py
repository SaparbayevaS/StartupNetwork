from typing import Optional, Any
from django.db.models import (
    BooleanField, EmailField, CharField,
    OneToOneField, IntegerField, CASCADE
)
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

from common.models import AbstactSoftDeletableModel
from common.constants import (
    USER_FULL_NAME_MAX_LENGTH,
    PROFILE_DEFAULT_COUNT,
)

class CustomUserManager(BaseUserManager):
    """
    Manager for CustomUser model.
    Used to create users and superusers.
    """

    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any):
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

    def create_superuser(self, email: str, password: Optional[str] = None, **extra_fields: Any):
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
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email


class UserProfile:
    """
    User profile model.
    Connected to CustomUser with one-to-one relation.
    """
    user = OneToOneField(CustomUser, on_delete=CASCADE, related_name='profile')
    total_ideas = IntegerField(default=PROFILE_DEFAULT_COUNT)
    total_comments = IntegerField(default=PROFILE_DEFAULT_COUNT)
    total_votes = IntegerField(default=PROFILE_DEFAULT_COUNT)