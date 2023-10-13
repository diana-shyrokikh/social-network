from django.contrib import admin
from django.contrib.auth import get_user_model

from social_network.models import Post

admin.site.register(get_user_model())
admin.site.register(Post)
