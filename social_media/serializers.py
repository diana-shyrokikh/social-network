from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_media.models import Post


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()

        fields = (
            "id",
            "last_login",
            "username",
            "password",
            "last_request",
            "likes_count",
        )

        read_only_fields = (
            "id",
            "last_login",
            "last_request",
            "likes_count",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()

        fields = (
            "username",
            "password",
        )

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            **validated_data
        )


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source="author.username", read_only=True
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "text",
            "author",
            "likes",
            "dislikes",
            "created_at",
        )
        read_only_fields = (
            "id",
            "likes",
            "dislikes",
            "created_at",
            "author",
        )
