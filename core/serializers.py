from rest_framework import serializers
from .models import Idea, Comment, Category, Vote

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)
    
    class Meta:
        model = Comment
        fields = "__all__"
        
class VoteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Vote
        fields = "__all__"

class IdeaSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)
    comments =CommentSerializer(many=True, read_only=True)
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = Idea
        fields = [
            "id",
            "title",
            "description",
            "status",
            "author_email",
            "comments",
            "categories",
            "created_at",
        ]
    def get_categories(self, obj):
        return [ic.category.name for ic in obj.idea_categories.all()]