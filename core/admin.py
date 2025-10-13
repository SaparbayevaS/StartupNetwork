from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import User,Category,Idea,IdeaCategory,Vote,Comment

@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ("id", "username", "email", "full_name", "bio", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["bio"]
    search_fields = ["username", "email", "full_name", "bio"]

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["description"]
    search_fields = ["name"]

@admin.register(Idea)
class IdeaAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "status", "author", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["status"]
    search_fields = ["title", "author"]

@admin.register(IdeaCategory)
class IdeaCategoryAdmin(ModelAdmin):
    list_display = ("id", "idea", "category", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["category"]
    search_fields = ["idea", "category"]

@admin.register(Comment)
class CommentyAdmin(ModelAdmin):
    list_display = ("id", "idea", "author", "content", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["content"]
    search_fields = ["idea", "author"]

@admin.register(Vote)
class VoteAdmin(ModelAdmin):
    list_display = ("id", "idea", "user", "is_upvote", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["is_upvote"]
    search_fields = ["idea", "user"]
