from rest_framework.serializers import ModelSerializer, EmailField, SerializerMethodField, HiddenField, PrimaryKeyRelatedField, CurrentUserDefault

from ideas.models import Idea, Comment, Category, Vote

class CategorySerializer(ModelSerializer):
    """
    Serializer for idea categories.
    """
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    """
    Serializer for comments on ideas.
    """
    author_email = EmailField(source='author.email', read_only=True)
    idea = PrimaryKeyRelatedField(queryset=Idea.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_email', 'idea', 'created_at', 'updated_at', 'deleted_at']


class VoteSerializer(ModelSerializer):
    """
    Serializer for votes on ideas.
    """
    user = HiddenField(default=CurrentUserDefault())
    idea = PrimaryKeyRelatedField(queryset=Idea.objects.all())

    class Meta:
        model = Vote
        fields = "__all__"


class IdeaSerializer(ModelSerializer):
    """
    Serializer for ideas.
    """
    author_email = EmailField(source='author.email', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category_name = SerializerMethodField()

    class Meta:
        model = Idea
        fields = [
            "id",
            "title",
            "description",
            "author_email",
            "comments",
            "category",
            "category_name",
            "created_at",
            "updated_at",
            "deleted_at"
        ]

    def get_category_name(self, obj: Idea) -> str | None:
        return obj.category.name if obj.category else None
