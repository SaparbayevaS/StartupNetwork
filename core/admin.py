from django.contrib import admin
from .models import User, Category, Idea, IdeaCategory, Comment

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Idea)
admin.site.register(IdeaCategory)
admin.site.register(Comment)

