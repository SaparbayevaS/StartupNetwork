from django.db import models

class AbstractSoftDeletableModel(models.Model):
    is_deleted = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

class User(AbstractSoftDeletableModel):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
class Category(AbstractSoftDeletableModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Idea(AbstractSoftDeletableModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='ideas')
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='IdeaCategory')

    def __str__(self):
        return self.title
    
class IdeaCategory(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.idea.title} - {self.category.name}"
    
class Comment(AbstractSoftDeletableModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    is_upvote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.idea.title}"