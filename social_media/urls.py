from django.urls import path, include
from rest_framework import routers

from social_media import views

router = routers.DefaultRouter()
router.register("users", views.UserViewSet)
router.register("posts", views.PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "singup/",
        views.CreateUserView.as_view(),
        name="signup"
    )
]

app_name = "social_media"
