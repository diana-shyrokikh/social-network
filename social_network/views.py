from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response

from social_network.models import (
    Post,
    PostUserReaction,
)
from social_network.paginations import TenSizePagination
from social_network.permissions import IsAuthorOrReadOnly
from social_network.serializers import (
    UserSerializer,
    PostSerializer,
    UserCreateSerializer,
    UserLikesAnalyticsSerializer
)
from social_network.utils import (
    is_user_post_author,
    like_or_dislike_post,
    like_or_dislike_post_update,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, ]
    pagination_class = TenSizePagination


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserActivityView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = TenSizePagination

    def get_queryset(self):
        queryset = get_user_model().objects.all()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                id=self.request.user.id
            )

        return queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = TenSizePagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=["GET"],
        detail=True,
        url_path="like",
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
        url_path="dislike",
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
    permission_classes = [IsAuthenticated, ]
    pagination_class = TenSizePagination

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
            ).values("date").annotate(total_likes=Count("id"))

            if not self.request.user.is_superuser:
                queryset = queryset.filter(user=self.request.user)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "date_from",
                type=str,
                description="Filter by date_from (ex. ?date_from=2023-10-10)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                "date_to",
                type=str,
                description="Filter by date_to (ex. ?date_to=2023-10-12)",
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

