from django.contrib import admin
from .models import UserProfile,Category,Idea,Vote,Comment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=('user','total_likes','is_deleted')
    search_fields=('user__username',)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','is_deleted')
    
@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display=('title','author','rating','views','is_deleted','created_at')
    search_fields=('title','description','author__username')
    list_filter=('readiness','category')
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display=('user','idea','value','is_deleted','created_at')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('author','idea','parent','is_deleted','created_at')
    search_fields=('content','author__username')