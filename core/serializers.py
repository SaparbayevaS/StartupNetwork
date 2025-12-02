from rest_framework.serializers import ModelSerializer, CharField, EmailField, SerializerMethodField, HiddenField, PrimaryKeyRelatedField, CurrentUserDefault
from core.models import CustomUser, Idea, Comment, Category, Vote
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)

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


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentSerializer(ModelSerializer):
    author_email = EmailField(source='author.email', read_only=True)
    idea = PrimaryKeyRelatedField(queryset=Idea.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_email', 'idea', 'created_at', 'updated_at', 'deleted_at']


class VoteSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    idea = PrimaryKeyRelatedField(queryset=Idea.objects.all())

    class Meta:
        model = Vote
        fields = "__all__"


class IdeaSerializer(ModelSerializer):
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

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None