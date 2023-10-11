from django.contrib.auth import get_user_model

from social_media.models import (
    Post,
    PostUserReaction,
)


def like_or_dislike_post(
    user: get_user_model(),
    post: Post,
    reaction: bool
) -> str:
    if not reaction:
        post.dislikes += 1
    else:
        post.likes += 1

    post.save()

    PostUserReaction.objects.create(
        user=user,
        post=post,
        is_liked=reaction
    )

    reaction = (
        "like" if reaction
        else "dislike"
    )

    return f"Post {reaction}d successfully"


def like_or_dislike_post_update(
    post: Post,
    post_user_table: PostUserReaction,
    reaction: bool
) -> str:
    if not reaction:
        post.likes -= 1
        post.dislikes += 1
    else:
        post.dislikes -= 1
        post.likes += 1

    post.save()
    post_user_table.is_liked = reaction
    post_user_table.save()

    reaction = (
        "like" if reaction
        else "dislike"
    )

    return f"Post {reaction}d successfully"
