from django.db import models
from django.utils import timezone


class AbstactSoftDeletableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    class Meta:
        abstract = True


class User(AbstactSoftDeletableModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=150)
    bio = models.TextField()

    def __str__(self):
        return self.username


class Category(AbstactSoftDeletableModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Idea(AbstactSoftDeletableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ideas")

    def __str__(self):
        return self.title


class IdeaCategory(AbstactSoftDeletableModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="idea_categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_ideas")

    def __str__(self):
        return f"{self.idea.title} - {self.category.name}"


class Comment(AbstactSoftDeletableModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author.username} on {self.idea.title}"


class Vote(AbstactSoftDeletableModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    is_upvote = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} → {self.idea.title} ({'Up' if self.is_upvote else 'Down'})"