from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from social_media import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("posts", views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    path(
        "signup/",
        views.CreateUserView.as_view(),
        name="signup"
    ),
    path(
        "user_activity/",
        views.UserActivityView.as_view(),
        name="user_activity"
    ),
    path(
        "analytics/",
        views.UserLikesAnalyticsView.as_view(),
        name="user_analytics"
    ),
]

app_name = "social_media"
