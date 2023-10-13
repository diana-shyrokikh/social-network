"""
WSGI config for social_media_api_service project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "social_media_api_service.settings"
)

application = get_wsgi_application()
