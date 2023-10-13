from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser with a specific password"

    def handle(self, *args, **options):
        username = "admin"
        email = "admin@admin.com"
        password = "admin123456"

        if get_user_model().objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                "Superuser already exists."
            ))
        else:
            get_user_model().objects.create_superuser(
                username, email, password
            )
            self.stdout.write(self.style.SUCCESS(
                f"Superuser '{username}' created successfully."
            ))
