from django.db.models import Model, BooleanField, DateTimeField, EmailField, CharField, TextField, OneToOneField, ImageField, CASCADE, ForeignKey, IntegerField, ManyToManyField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class AbstactSoftDeletableModel(Model):
    """
    Your docstring text.
    """
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = DateTimeField(null=True, blank=True)
    
    def delete(self, using: str = None, keep_parents: bool = False) -> None:
        """..."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
           
    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstactSoftDeletableModel):
    email = EmailField(unique=True)
    full_name = CharField(max_length=150, blank=True)
    bio = TextField(blank=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


class UserProfile(AbstractBaseUser):
    user = OneToOneField(CustomUser, on_delete=CASCADE, related_name='profile')
    avatar = ImageField(upload_to='avatars/', null=True, blank=True)
    total_likes = IntegerField(default=0)

    def __str__(self):
        return self.user.email


class Category(AbstactSoftDeletableModel):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class Idea(AbstactSoftDeletableModel):
    title = CharField(max_length=200)
    description = TextField()
    category = ForeignKey(Category, on_delete=CASCADE, related_name='ideas')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='ideas')

    def __str__(self):
        return self.title


class Comment(AbstactSoftDeletableModel):
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='comments')
    author = ForeignKey(CustomUser, on_delete=CASCADE, related_name='comments')
    content = TextField()

    def __str__(self):
        return f"{self.author.email} on {self.idea.title}"


class Vote(AbstactSoftDeletableModel):
    idea = ForeignKey(Idea, on_delete=CASCADE, related_name='votes')
    user = ForeignKey(CustomUser, on_delete=CASCADE, related_name='votes')

    class Meta:
        unique_together = ('idea', 'user')

    def __str__(self):
        return f"{self.user.email} voted on {self.idea.title}"