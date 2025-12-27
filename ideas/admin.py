from django.contrib.admin import ModelAdmin, register
from .models import Category, Idea, Comment, Vote

@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Admin interface for category
    """
    list_display = ("name", "created_at", "updated_at", "deleted_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Idea)
class IdeaAdmin(ModelAdmin):
    """
    Admin interface for idea
    """
    list_display = ("title", "author", "category", "created_at", "updated_at", "deleted_at")
    list_filter = ("category", "author")
    search_fields = ("title", "description", "author__email")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Admin interface for comment
    """
    list_display = ("idea", "author", "content", "created_at", "updated_at", "deleted_at")
    search_fields = ("content", "author__email", "idea__title")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Vote)
class VoteAdmin(ModelAdmin):
    """
    Admin interface for vote
    """
    list_display = ("idea", "user", "created_at", "updated_at", "deleted_at")
    search_fields = ("user__email", "idea__title")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
