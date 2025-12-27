from typing import Any, Dict
from rest_framework.serializers import ModelSerializer, CharField, EmailField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser, UserProfile

class RegisterSerializer(ModelSerializer):
    """
    Serializer for registering a new user.
    """
    password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "full_name", "password"]

    def create(self, validated_data: Dict[str, Any]) -> CustomUser:
        """
        Create and return a new user with encrypted password.
        """
        return CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", "")
        )


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for containing JWT token on login.
    """
    @classmethod
    def get_token(cls, user: CustomUser) -> Any:
        """
        Return a token with user's email and full name included.
        """
        token = super().get_token(user)
        token["email"] = user.email
        token["full_name"] = user.full_name
        return token


class UserProfileSerializer(ModelSerializer):
    """
    Serializer for user's profile statistics.
    """
    user_email = EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user_email',
            'total_ideas',
            'total_comments',
            'total_votes'
        ]
