"""Management command to bootstrap dummy data for firewall model app."""

from django.core.management.base import BaseCommand

from nautobot_firewall_models.tests.fixtures import create_capirca_env, create_firewall_config_env


class Command(BaseCommand):
    """Publish command to bootstrap dummy data."""

    def handle(self, *args, **options):
        """Publish command to bootstrap dummy data."""
        self.stdout.write("Attempting to populate dummy data.")
        create_capirca_env()
        create_firewall_config_env()
        self.stdout.write(self.style.SUCCESS("Successfully populated dummy data!"))
