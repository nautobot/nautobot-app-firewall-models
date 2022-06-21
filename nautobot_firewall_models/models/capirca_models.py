import imp
from django.db import models
from django.urls import reverse
from django.utils.module_loading import import_string
from nautobot.extras.utils import extras_features


from nautobot_firewall_models.capirca_utils import DevicePolicyToCapirca
from nautobot_firewall_models.constants import PLUGIN_CFG
from nautobot.core.models.generics import PrimaryModel


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
class CapircaPolicy(PrimaryModel):
    """CapircaPolicy model."""

    device = models.OneToOneField(to="dcim.Device", blank=True, null=True, on_delete=models.CASCADE)
    pol = models.TextField(blank=True, null=True)
    net = models.TextField(blank=True, null=True)
    svc = models.TextField(blank=True, null=True)
    cfg = models.TextField(blank=True, null=True)

    csv_headers = ["device"]

    class Meta:
        """Meta class."""

        ordering = ["device"]
        verbose_name_plural = "Capirca Policies"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:capircapolicy", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.device.name

    def save(self, *args, **kwargs):
        """Update the firewall rules as updates are made."""
        if not PLUGIN_CFG.get("custom_capirca"):
            cap_obj = DevicePolicyToCapirca(self.device)
            cap_obj.get_all_capirca_cfg()
            self.pol = cap_obj.pol_file
            self.svc = cap_obj.svc_file
            self.net = cap_obj.net_file
            self.cfg = cap_obj.cfg_file
        else:
            self.pol, self.svc, self.net, self.cfg = import_string(PLUGIN_CFG["custom_capirca"])(self.device)

        super().save(*args, **kwargs)
