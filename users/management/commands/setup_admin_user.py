import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update an admin superuser from environment variables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            default=os.getenv("ADMIN_USERNAME", "admin"),
            help="Admin username. Defaults to ADMIN_USERNAME or admin.",
        )
        parser.add_argument(
            "--password",
            default=os.getenv("ADMIN_PASSWORD"),
            help="Admin password. Defaults to ADMIN_PASSWORD.",
        )
        parser.add_argument(
            "--email",
            default=os.getenv("ADMIN_EMAIL", "admin@example.com"),
            help="Admin email. Defaults to ADMIN_EMAIL or admin@example.com.",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        email = options["email"]

        if not username:
            raise CommandError("ADMIN_USERNAME is required.")

        if not password:
            raise CommandError("ADMIN_PASSWORD is required.")

        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email},
        )
        user.email = user.email or email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} admin user: {username}"
            )
        )
