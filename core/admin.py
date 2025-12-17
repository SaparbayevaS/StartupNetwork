from django.contrib.admin import ModelAdmin, register
from .models import CustomUser, UserProfile, Category, Idea, Comment, Vote

@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """
    Admin interface for CustomUser
    """
    list_display = ("email", "full_name", "is_staff", "is_active", "created_at", "updated_at", "deleted_at")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "full_name")
    readonly_fields = ("created_at", "updated_at", "deleted_at")
    ordering = ("-created_at",)

@register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    """
    Admin interface for UserProfile
    """
    list_display = ("user", "ideas_count", "comments_count", "votes_count")
    search_fields = ("user__email",)

    def ideas_count(self, obj):
        """
        Returns the total number of ideas created by the user
        """
        return obj.user.ideas.count()
    ideas_count.short_description = "Ideas"

    def comments_count(self, obj):
        """
        Returns the total number of comments created by the user
        """
        return obj.user.comments.count()
    comments_count.short_description = "Comments"

    def votes_count(self, obj):
        """
        Returns the total number of votes made by the user
        """
        return obj.user.votes.count()
    votes_count.short_description = "Votes"

@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Admin interface for сategory
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