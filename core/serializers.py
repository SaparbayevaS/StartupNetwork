from rest_framework import serializers
<<<<<<< HEAD
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
    
=======
from core.models import CustomUser, Idea, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "full_name", "bio"]

class IdeaSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

>>>>>>> origin/bekarys
    class Meta:
        model = Idea
        fields = [
            "id",
            "title",
            "description",
            "status",
<<<<<<< HEAD
            "author_email",
            "comments",
            "categories",
            "created_at",
        ]
    def get_categories(self, obj):
        return [ic.category.name for ic in obj.idea_categories.all()]
=======
            "author",
            "created_at",
            "updated_at",
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "idea",
            "author",
            "content",
            "created_at",
            "updated_at",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", "")
        )

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["full_name"] = user.full_name

        return token
>>>>>>> origin/bekarys
