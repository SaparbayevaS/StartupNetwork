from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

from unfold.admin import ModelAdmin
from .models import CustomUser, Category, Idea, Comment, Vote

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'bio')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'bio', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)

    ordering = ('email',)

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ("id", "email", "full_name", "bio", "is_staff", "is_active", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email", "full_name", "bio"]

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["name"]
    search_fields = ["name", "description"]

@admin.register(Idea)
class IdeaAdmin(ModelAdmin):
    list_display = ("id", "title", "description", "status", "author", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["status"]
    search_fields = ["title", "author__email"]

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ("id", "idea", "author", "content", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["idea"]
    search_fields = ["content", "author__email"]

@admin.register(Vote)
class VoteAdmin(ModelAdmin):
    list_display = ("id", "idea", "user", "is_upvote", "created_at", "updated_at", "is_deleted", "deleted_at")
    list_filter = ["is_upvote"]
    search_fields = ["user__email", "idea__title"]

