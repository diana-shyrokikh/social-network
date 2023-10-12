from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response

from social_media.models import (
    Post,
    PostUserReaction,
)
from social_media.serializers import (
    UserSerializer,
    PostSerializer,
    UserCreateSerializer,
    UserActivitySerializer,
    UserLikesAnalyticsSerializer
)
from social_media.utils import (
    is_user_post_author,
    like_or_dislike_post,
    like_or_dislike_post_update,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserActivityView(generics.ListAPIView):
    serializer_class = UserActivitySerializer

    def get_queryset(self):
        return get_user_model().objects.filter(
            id=self.request.user.id
        )


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
        message = is_user_post_author(
            post, user, True
        )

        if not message:

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
        message = is_user_post_author(
            post, user, False
        )

        if not message:
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


class UserLikesAnalyticsView(generics.ListAPIView):
    serializer_class = UserLikesAnalyticsSerializer

    def get_queryset(self):
        queryset = PostUserReaction.objects.select_related(
            "user", "post"
        )
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from and date_to:
            queryset = queryset.filter(
                (Q(date__gte=date_from) & Q(date__lte=date_to)),
                is_liked=True,
                user=self.request.user,
            ).values("date").annotate(total_likes=Count("id"))

        return queryset
