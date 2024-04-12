"""Models for the Aerleon Configurations."""
# pylint: disable=duplicate-code
import logging

from django.db import models
from django.utils.module_loading import import_string
from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.utils import extras_features

from nautobot_firewall_models.constants import PLUGIN_CFG
from nautobot_firewall_models.utils.aerleon import DevicePolicyToAerleon

LOGGER = logging.getLogger(__name__)


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
class AerleonPolicy(PrimaryModel):
    """AerleonPolicy model."""

    device = models.OneToOneField(
        to="dcim.Device", blank=True, null=True, on_delete=models.CASCADE, related_name="aerleon_policy"
    )
    pol = models.TextField(blank=True)
    net = models.TextField(blank=True)
    svc = models.TextField(blank=True)
    cfg = models.TextField(blank=True)

    csv_headers = ["device"]

    class Meta:
        """Meta class."""

        ordering = ["device"]
        verbose_name_plural = "Aerleon Policies"

    def __str__(self):
        """Stringify instance."""
        return f"Aerleon Policy -> {self.device.name}"

    def save(self, *args, **kwargs):
        """Update the firewall rules as updates are made."""
        if not PLUGIN_CFG.get("custom_aerleon"):
            LOGGER.debug("Running standard Aerleon conversion")
            cap_obj = DevicePolicyToAerleon(self.device)
            cap_obj.get_all_aerleon_cfg()
            self.pol = cap_obj.pol_file
            self.svc = cap_obj.svc_file
            self.net = cap_obj.net_file
            self.cfg = cap_obj.cfg_file
        else:
            LOGGER.debug("Running custom conversion from function: `%s`", str(PLUGIN_CFG["custom_aerleon"]))
            self.pol, self.svc, self.net, self.cfg = import_string(PLUGIN_CFG["custom_aerleon"])(self.device)

        super().save(*args, **kwargs)
