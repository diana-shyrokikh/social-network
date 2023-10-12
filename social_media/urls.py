from django.urls import path, include
from rest_framework import routers

from social_media import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("posts", views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "signup/",
        views.CreateUserView.as_view(),
        name="signup"
    )
    ),
    path(
        "user_activity/",
        views.UserActivityView.as_view(),
        name="user_activity"
    ),
]

app_name = "social_media"
