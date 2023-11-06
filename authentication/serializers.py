from typing import Dict, Any

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration that includes password confirmation.

    Attributes:
        password_confirm: A field for the password confirmation,
            which is write-only and not saved to the model.
    """

    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", 'email', "password", "password_confirm")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the password and password_confirm fields match.

        Args:
            data: Input data for validation.

        Returns:
            Dict: Validated data.

        Raises:
            ValidationError: If the password and password_confirm fields do not match.
        """

        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": ["Passwords do not match."]}
            )
        return data

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Create a new user instance.

        Args:
            validated_data: Data that has passed validation.

        Returns:
            User: A new user instance.
        """

        validated_data.pop("password_confirm")
        return User.objects.create_user(**validated_data)


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('last_login', 'last_request')
        read_only_fields = fields


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)

        self.context['view'].user = self.user

        return data