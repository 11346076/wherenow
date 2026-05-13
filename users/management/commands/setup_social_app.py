from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensure Site record exists (Google OAuth credentials come from env, not DB)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            default='127.0.0.1:8000',
            help='Domain for the Site record (default: 127.0.0.1:8000)'
        )
        parser.add_argument(
            '--name',
            default='WhereNow Dev',
            help='Name for the Site record (default: WhereNow Dev)'
        )

    def handle(self, *args, **options):
        site, created = Site.objects.update_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': options['domain'],
                'name': options['name'],
            }
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"{'Created' if created else 'Updated'} Site: "
                f"id={site.id}, domain={site.domain}"
            )
        )
