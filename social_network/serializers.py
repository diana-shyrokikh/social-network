from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_network.models import Post


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
        )

        read_only_fields = (
            "id",
            "last_login",
            "last_request",
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


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = (
            "id",
            "username",
            "last_login",
            "last_request",
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


class UserLikesAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_likes = serializers.IntegerField()

    class Meta:
        fields = (
            "date",
            "total_likes",
        )
