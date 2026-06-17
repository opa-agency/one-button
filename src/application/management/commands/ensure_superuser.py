import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from env vars if one does not already exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        missing = [
            name
            for name, value in (
                ("DJANGO_SUPERUSER_USERNAME", username),
                ("DJANGO_SUPERUSER_EMAIL", email),
                ("DJANGO_SUPERUSER_PASSWORD", password),
            )
            if not value
        ]
        if missing:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser bootstrap; missing env vars: "
                    + ", ".join(missing)
                )
            )
            return

        user_model = get_user_model()
        lookup = {user_model.USERNAME_FIELD: username}
        user, created = user_model._default_manager.get_or_create(
            **lookup,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        if created:
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save(update_fields=["email", "is_staff", "is_superuser", "password"])
            self.stdout.write(
                self.style.SUCCESS(f"Created admin user '{username}'.")
            )
            return

        changed = False
        if email and user.email != email:
            user.email = email
            changed = True
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True

        if changed:
            user.save(update_fields=["email", "is_staff", "is_superuser"])

        self.stdout.write(
            self.style.SUCCESS(f"Admin user '{username}' already exists.")
        )