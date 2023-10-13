"""
URL configuration for social_media_api_service project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/v1/social_media/", include(
        "social_media.urls", namespace="social_media"
    ))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
