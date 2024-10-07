"""Configurable signals."""

from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from nautobot.dcim.models import Interface
from nautobot.ipam.models import VRF, IPAddress, Prefix

from nautobot_firewall_models import models
from nautobot_firewall_models.constants import PLUGIN_CFG
from nautobot_firewall_models.utils import create_configured_statuses

ON_DELETE = {
    IPAddress: ["fqdns", "address_objects"],
    Prefix: ["address_objects"],
    VRF: ["zones"],
    Interface: ["zones"],
    models.FQDN: ["address_objects"],
    models.IPRange: ["address_objects"],
    models.AddressObject: [
        "address_object_groups",
        "source_policy_rules",
        "destination_policy_rules",
        "original_source_nat_policy_rules",
        "translated_source_nat_policy_rules",
        "original_destination_nat_policy_rules",
        "translated_destination_nat_policy_rules",
    ],
    models.AddressObjectGroup: [
        "source_policy_rules",
        "destination_policy_rules",
        "original_source_nat_policy_rules",
        "translated_source_nat_policy_rules",
        "original_destination_nat_policy_rules",
        "translated_destination_nat_policy_rules",
    ],
    models.ServiceObject: [
        "service_object_groups",
        "source_policy_rules",
        "destination_policy_rules",
        "original_source_nat_policy_rules",
        "translated_source_nat_policy_rules",
        "original_destination_nat_policy_rules",
        "translated_destination_nat_policy_rules",
    ],
    models.ServiceObjectGroup: [
        "source_policy_rules",
        "destination_policy_rules",
        "original_source_nat_policy_rules",
        "translated_source_nat_policy_rules",
        "original_destination_nat_policy_rules",
        "translated_destination_nat_policy_rules",
    ],
    models.ApplicationObject: [
        "application_object_groups",
        "destination_policy_rules",
    ],
    models.ApplicationObjectGroup: [
        "destination_policy_rules",
    ],
    models.UserObject: [
        "user_object_groups",
        "policy_rules",
    ],
    models.UserObjectGroup: [
        "policy_rules",
    ],
    models.Zone: [
        "source_policy_rules",
        "destination_policy_rules",
        "source_nat_policy_rules",
        "destination_nat_policy_rules",
    ],
    models.PolicyRule: [
        "policies",
    ],
    models.NATPolicyRule: [
        "nat_policies",
    ],
}

if PLUGIN_CFG["protect_on_delete"]:

    @receiver(pre_delete, sender=IPAddress)
    @receiver(pre_delete, sender=Prefix)
    @receiver(pre_delete, sender=VRF)
    @receiver(pre_delete, sender=Interface)
    @receiver(pre_delete, sender=models.FQDN)
    @receiver(pre_delete, sender=models.IPRange)
    @receiver(pre_delete, sender=models.AddressObject)
    @receiver(pre_delete, sender=models.AddressObjectGroup)
    @receiver(pre_delete, sender=models.ServiceObject)
    @receiver(pre_delete, sender=models.ServiceObjectGroup)
    @receiver(pre_delete, sender=models.ApplicationObject)
    @receiver(pre_delete, sender=models.ApplicationObjectGroup)
    @receiver(pre_delete, sender=models.UserObject)
    @receiver(pre_delete, sender=models.UserObjectGroup)
    @receiver(pre_delete, sender=models.Zone)
    @receiver(pre_delete, sender=models.PolicyRule)
    @receiver(pre_delete, sender=models.NATPolicyRule)
    def on_delete_handler(instance, **kwargs):
        """Signal handler to enable on_delete=PROTECT."""
        for i in ON_DELETE[instance._meta.model]:
            if hasattr(instance, i) and getattr(instance, i).exists():
                raise ValidationError(f"{instance} is assigned to an {i} & `protect_on_delete` is enabled.")


def create_configured_statuses_signal(sender, **kwargs):
    """Signal handler to create default_status and allowed_status configured in the app config."""
    create_configured_statuses()
