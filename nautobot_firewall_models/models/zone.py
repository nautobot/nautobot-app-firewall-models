"""Models for the Firewall app."""
# pylint: disable=duplicate-code

from django.db import models
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

from nautobot_firewall_models.utils import get_default_status

###########################
# Core Models
###########################


@extras_features(
    "custom_fields",
    "custom_links",
    "custom_validators",
    "export_templates",
    "graphql",
    "relationships",
    "statuses",
    "webhooks",
)
class Zone(PrimaryModel):
    """Zones common on firewalls and are typically seen as representations of area (e.g. DMZ trust untrust)."""

    description = models.CharField(
        max_length=1024,
        blank=True,
    )
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True, help_text="Name of the zone (e.g. trust)")
    vrfs = models.ManyToManyField(to="ipam.VRF", blank=True, related_name="zones")
    interfaces = models.ManyToManyField(to="dcim.Interface", blank=True, related_name="zones")
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def __str__(self):
        """Stringify instance."""
        return self.name
