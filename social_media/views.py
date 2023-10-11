from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from social_media.models import (
    Post,
    PostUserReaction,
)
from social_media.serializers import (
    UserSerializer,
    PostSerializer,
    UserCreateSerializer
)
from social_media.utils import (
    like_or_dislike_post,
    like_or_dislike_post_update,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["GET"],
        detail=True,
        url_path="like-post",
        permission_classes=[IsAuthenticated, ],
    )
    def like_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        is_reacted_before = PostUserReaction.objects.filter(
            user=user, post=post
        )

        if is_reacted_before:
            reaction = is_reacted_before[0].is_liked

            if reaction:
                message = "You cannot like the post twice"
            else:
                message = like_or_dislike_post_update(
                    post, is_reacted_before[0], True
                )

        else:
            message = like_or_dislike_post(user, post, True)

        return Response({
            "message": message
        })

    @action(
        methods=["GET"],
        detail=True,
        url_path="dislike-post",
        permission_classes=[IsAuthenticated, ],
    )
    def dislike_post(self, request, pk=None):
        post = self.get_object()
        user = request.user
        is_reacted_before = PostUserReaction.objects.filter(
            user=user, post=post
        )

        if is_reacted_before:
            reaction = is_reacted_before[0].is_liked

            if not reaction:
                message = "You cannot dislike the post twice"
            else:
                message = like_or_dislike_post_update(
                    post, is_reacted_before[0], False
                )

        else:
            message = like_or_dislike_post(user, post, False)

        return Response({
                "message": message
            })
