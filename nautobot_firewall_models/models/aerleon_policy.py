"""Models for the Aerleon Configurations."""

# pylint: disable=duplicate-code
import logging

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.module_loading import import_string
from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.utils import extras_features

from nautobot_firewall_models.constants import PLUGIN_CFG
from nautobot_firewall_models.utils.aerleon import ObjectPolicyToAerleon

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

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    attached_object = GenericForeignKey()
    pol = models.TextField(blank=True)
    net = models.TextField(blank=True)
    svc = models.TextField(blank=True)
    cfg = models.TextField(blank=True)

    csv_headers = ["object_id", "content_type"]
    natural_key_field_names = ["pk"]

    class Meta:
        """Meta class."""

        ordering = ["pk"]
        verbose_name_plural = "Aerleon Policies"
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def __str__(self):
        """Stringify instance."""
        return f"Aerleon Policy -> {self.attached_object.name}"

    def save(self, *args, **kwargs):
        """Update the firewall rules as updates are made."""
        if not PLUGIN_CFG.get("custom_aerleon"):
            LOGGER.debug("Running standard Aerleon conversion")
            aerleon_obj = ObjectPolicyToAerleon(self.attached_object)
            aerleon_obj.get_all_aerleon_cfg()
            self.pol = aerleon_obj.pol_file
            self.svc = aerleon_obj.svc_file
            self.net = aerleon_obj.net_file
            self.cfg = aerleon_obj.cfg_file
        else:
            LOGGER.debug("Running custom conversion from function: `%s`", str(PLUGIN_CFG["custom_aerleon"]))
            self.pol, self.svc, self.net, self.cfg = import_string(PLUGIN_CFG["custom_aerleon"])(self.attached_object)

        super().save(*args, **kwargs)
