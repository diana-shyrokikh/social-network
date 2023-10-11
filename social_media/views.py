from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics

from social_media.models import Post
from social_media.serializers import (
    UserSerializer,
    PostSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

