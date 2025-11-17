"""Models for the Capirca Configurations."""

# pylint: disable=duplicate-code
import logging

from django.db import models
from django.utils.module_loading import import_string
from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.utils import extras_features

from nautobot_firewall_models.choices import FirewallConfigChoice
from nautobot_firewall_models.constants import PLUGIN_CFG
from nautobot_firewall_models.utils.aerleon import DevicePolicyToAerleon
from nautobot_firewall_models.utils.capirca import DevicePolicyToCapirca

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
class FirewallConfig(PrimaryModel):
    """FirewallConfig model."""

    device = models.OneToOneField(
        to="dcim.Device", blank=True, null=True, on_delete=models.CASCADE, related_name="firewall_config"
    )
    firewall_config_type = models.CharField(
        max_length=50,
        default=PLUGIN_CFG["default_driver"],
        choices=FirewallConfigChoice,
        help_text="Whether the firewall config type is CAPIRCA, AERLEON, or custom.",
    )
    pol = models.TextField(blank=True)
    net = models.TextField(blank=True)
    svc = models.TextField(blank=True)
    cfg = models.TextField(blank=True)

    csv_headers = ["device"]

    class Meta:
        """Meta class."""

        ordering = ["device"]
        verbose_name_plural = "Firewall Configs"

    def __str__(self):
        """Stringify instance."""
        return f"Firewall Config -> {self.device.name}"

    def save(self, *args, **kwargs):
        """Update the firewall rules as updates are made."""
        if self.firewall_config_type == FirewallConfigChoice.TYPE_AERLEON:
            LOGGER.debug("Running Aerleon conversion")
            aerleon_obj = DevicePolicyToAerleon(self.device)
            aerleon_obj.get_all_aerleon_cfg()
            self.pol = aerleon_obj.pol_file
            self.svc = aerleon_obj.svc_file
            self.net = aerleon_obj.net_file
            self.cfg = aerleon_obj.cfg_file
        elif self.firewall_config_type == FirewallConfigChoice.TYPE_CAPIRCA:
            LOGGER.debug("Running standard Capirca conversion")
            capirca_obj = DevicePolicyToCapirca(self.device, _legacy_map=False)
            capirca_obj.get_all_capirca_cfg()
            self.pol = capirca_obj.pol_file
            self.svc = capirca_obj.svc_file
            self.net = capirca_obj.net_file
            self.cfg = capirca_obj.cfg_file
        elif self.firewall_config_type == FirewallConfigChoice.TYPE_CUSTOM:
            path = PLUGIN_CFG.get("custom_firewall_config")
            if not path:
                path = PLUGIN_CFG.get("custom_capirca")
            if not path:
                raise ValueError(
                    "Custom Config set, but not found in either `custom_firewall_config` or `custom_capirca` in app settings."
                )
            LOGGER.debug("Running custom conversion from function: `%s`", str(path))
            self.pol, self.svc, self.net, self.cfg = import_string(path)(self.device)
        else:
            LOGGER.warning(
                "firewall_config_type is set to an invalid value of `%s` on FirewallConfig for device `%s`",
                self.firewall_config_type,
                self.device.name,
            )

        super().save(*args, **kwargs)
