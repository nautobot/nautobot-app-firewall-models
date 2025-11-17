"""
Management command to migrate CapircaPolicy objects to FirewallConfig objects.

Usage:
    nautobot-server capirca_to_fw_config_migration
    nautobot-server capirca_to_fw_config_migration --commit # Flag to actually write changes

This script will copy all CapircaPolicy objects to FirewallConfig, if not already present.
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from nautobot.core.exceptions import AbortTransaction

from nautobot_firewall_models.constants import CAPIRCA_MAPPER
from nautobot_firewall_models.models.capirca_policy import CapircaPolicy
from nautobot_firewall_models.models.firewall_config import FirewallConfig


class Command(BaseCommand):
    """Management command to migrate CapircaPolicy objects to FirewallConfig objects."""

    help = "Migrate CapircaPolicy objects to FirewallConfig objects. By default, this is a dry run. Use --commit to write changes."

    def add_arguments(self, parser):
        """Add command line arguments to the parser."""
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Actually write changes to the database. By default, this is a dry run.",
        )

    def handle(self, *args, **options):
        """Handle the migration of CapircaPolicy objects to FirewallConfig objects."""
        migrated = 0
        skipped = 0
        dry_run = not options.get("commit", False)
        default_driver = settings.PLUGINS_CONFIG["nautobot_firewall_models"]["default_driver"]
        if dry_run:
            self.stdout.write(
                self.style.WARNING("Dry run mode: No changes will be written. Use --commit to apply changes.")
            )
        try:
            with transaction.atomic():
                for capirca in CapircaPolicy.objects.all():
                    if not capirca.device:
                        self.stdout.write(self.style.WARNING(f"CapircaPolicy {capirca.pk} has no device, skipping."))
                        skipped += 1
                        continue
                        # --- Platform mapping check (non-legacy only) ---
                    network_driver = getattr(getattr(capirca.device, "platform", None), "network_driver", None)
                    # If platform is not in CAPIRCA_MAPPER and not in device.platform.network_driver_mappings["capirca"], skip
                    is_new_platform = False
                    if network_driver:
                        mapping_driver = getattr(capirca.device.platform, "network_driver_mappings", {}).get("capirca")
                        if CAPIRCA_MAPPER.get(mapping_driver):
                            is_new_platform = True
                    if not is_new_platform:
                        self.stdout.write(
                            self.style.WARNING(
                                f"CapircaPolicy for device {capirca.device} skipped: platform '{capirca.device.platform}' does not meet new mapping condition."
                            )
                        )
                        skipped += 1
                        continue
                    if FirewallConfig.objects.filter(device=capirca.device).exists():
                        self.stdout.write(
                            self.style.WARNING(f"FirewallConfig already exists for device {capirca.device}, skipping.")
                        )
                        skipped += 1
                        continue
                    msg = (
                        f"Would migrate CapircaPolicy for device {capirca.device}"
                        if dry_run
                        else f"Migrated CapircaPolicy for device {capirca.device}"
                    )
                    fw_config = FirewallConfig(
                        device=capirca.device,
                        firewall_config_type=default_driver,
                        pol=capirca.pol,
                        net=capirca.net,
                        svc=capirca.svc,
                        cfg=capirca.cfg,
                    )
                    fw_config.save()
                    self.stdout.write(self.style.SUCCESS(msg))
                    migrated += 1
                if dry_run:
                    raise AbortTransaction("Dry run: rolling back all changes.")
        except AbortTransaction as e:
            self.stdout.write(self.style.WARNING(str(e)))
        self.stdout.write(
            self.style.SUCCESS(
                f"Migration complete. {'Would migrate' if dry_run else 'Migrated'}: {migrated}, Skipped: {skipped}"
            )
        )
