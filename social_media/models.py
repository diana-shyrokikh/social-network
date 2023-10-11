from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    last_request = models.DateTimeField(
        default=datetime.now()
    )
    likes_count = models.IntegerField(default=0)


class Post(models.Model):
    text = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        null=True, auto_now_add=True
    )
    author = models.ForeignKey(
        to=get_user_model(),
        related_name="posts",
        on_delete=models.CASCADE
    )

