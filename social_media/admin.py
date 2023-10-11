from django.contrib import admin
from django.contrib.auth import get_user_model

from social_media.models import Post

admin.site.register(get_user_model())
admin.site.register(Post)
