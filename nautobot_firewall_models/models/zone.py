"""Models for the Firewall plugin."""
# pylint: disable=duplicate-code

from django.db import models
from django.urls import reverse
from nautobot.core.models.generics import BaseModel, PrimaryModel
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
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True, help_text="Name of the zone (e.g. trust)")
    vrfs = models.ManyToManyField(to="ipam.VRF", blank=True, through="ZoneVRFM2M", related_name="zones")
    interfaces = models.ManyToManyField(
        to="dcim.Interface", blank=True, through="ZoneInterfaceM2M", related_name="zones"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:zone", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


###########################
# Through Models
###########################


class ZoneInterfaceM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated Interface if assigned to a Zone."""

    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.CASCADE)
    interface = models.ForeignKey("dcim.Interface", on_delete=models.PROTECT)


class ZoneVRFM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated VRF if assigned to a Zone."""

    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.CASCADE)
    vrf = models.ForeignKey("ipam.vrf", on_delete=models.PROTECT)
