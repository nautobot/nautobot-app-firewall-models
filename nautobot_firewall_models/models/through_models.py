"""Set of through intermediate models."""

from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from nautobot.core.models.generics import BaseModel


class AddressObjectGroupM2M(BaseModel):
    # pylint: disable=R0901
    """Custom through model to on_delete=models.PROTECT."""
    address = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    address_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)


class DestAddrGroupM2M(BaseModel):
    # pylint: disable=R0901
    """Custom through model to on_delete=models.PROTECT."""
    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class DestAddrM2M(BaseModel):
    # pylint: disable=R0901
    """Custom through model to on_delete=models.PROTECT."""
    user = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class FQDNIPAddressM2M(BaseModel):
    # pylint: disable=R0901
    """Custom through model to on_delete=models.PROTECT."""
    fqdn = models.ForeignKey("nautobot_firewall_models.FQDN", on_delete=models.PROTECT)
    ip_address = models.ForeignKey("ipam.IPAddress", on_delete=models.PROTECT)


class PolicyDeviceM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & Device relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.PROTECT)
    device = models.ForeignKey("dcim.Device", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "device"]


class PolicyDynamicGroupM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & DynamicGroup relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.PROTECT)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "dynamic_group"]


class PolicyRuleM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & PolicyRule relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.PROTECT)
    rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)
    index = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        """Meta class."""

        ordering = ["index"]
        constraints = [
            UniqueConstraint(fields=["policy", "rule", "index"], name="unique_with_index"),
            UniqueConstraint(fields=["policy", "rule"], name="unique_without_index", condition=Q(index=None)),
        ]


class ServiceObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    service = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    service_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)


class SrcAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    addr = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class SrcAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class SrcUserM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class SrcUserGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class SvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class SvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class UserObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.PROTECT)


class ZoneInterfaceM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.PROTECT)
    interface = models.ForeignKey("dcim.Interface", on_delete=models.PROTECT)


class ZoneVRFM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT."""

    # pylint: disable=R0901
    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.PROTECT)
    vrf = models.ForeignKey("ipam.vrf", on_delete=models.PROTECT)
