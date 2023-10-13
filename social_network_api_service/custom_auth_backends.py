from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone


class CustomAuthBackend(ModelBackend):
    def authenticate(
        self, request, username=None, password=None, **kwargs
    ):
        try:
            user = get_user_model().objects.get(username=username)
            if user.check_password(password):
                user.last_login = timezone.now()
                user.save()
                return user
        except get_user_model().DoesNotExist:
            return None
