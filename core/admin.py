from django.contrib.admin import ModelAdmin, register
from .models import CustomUser, UserProfile, Category, Idea, Comment, Vote

@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ("email", "full_name", "is_staff", "is_active", "created_at", "updated_at", "deleted_at")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("-created_at",)

@register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = ("user", "total_likes", "avatar")
    search_fields = ("user__email", "user__full_name")

@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "deleted_at")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Idea)
class IdeaAdmin(ModelAdmin):
    list_display = ("title", "author", "category", "created_at", "updated_at", "deleted_at")
    list_filter = ("category", "author")
    search_fields = ("title", "description", "author__email")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("idea", "author", "content", "created_at", "updated_at", "deleted_at")
    search_fields = ("content", "author__email", "idea__title")
    readonly_fields = ("created_at", "updated_at", "deleted_at")

@register(Vote)
class VoteAdmin(ModelAdmin):
    list_display = ("idea", "user", "created_at", "updated_at", "deleted_at")
    search_fields = ("user__email", "idea__title")
    readonly_fields = ("created_at", "updated_at", "deleted_at")