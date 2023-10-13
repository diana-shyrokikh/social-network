from django.contrib.auth import get_user_model

from social_network.models import (
    Post,
    PostUserReaction,
)


def is_user_post_author(
        post: Post,
        user: get_user_model(),
        is_liked: bool,
) -> str | None:
    is_liked = (
        "like" if is_liked
        else "dislike"
    )

    if post.author_id == user.id:
        return f"You cannot {is_liked} your post"


def like_or_dislike_post(
    user: get_user_model(),
    post: Post,
    is_liked: bool
) -> str:
    if not is_liked:
        post.dislikes += 1
    else:
        post.likes += 1

    post.save()

    PostUserReaction.objects.create(
        user=user,
        post=post,
        is_liked=is_liked
    )

    is_liked = (
        "like" if is_liked
        else "dislike"
    )

    return f"Post {is_liked}d successfully"


def like_or_dislike_post_update(
    post: Post,
    post_user_table: PostUserReaction,
    is_liked: bool
) -> str:
    if not is_liked:
        post.likes -= 1
        post.dislikes += 1
    else:
        post.dislikes -= 1
        post.likes += 1

    post.save()
    post_user_table.is_liked = is_liked
    post_user_table.save()

    is_liked = (
        "like" if is_liked
        else "dislike"
    )

    return f"Post {is_liked}d successfully"
