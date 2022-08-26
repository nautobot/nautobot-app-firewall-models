"""Set of through intermediate models."""

from django.db import models
from nautobot.core.models.generics import BaseModel


class AddressObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated AddressObject if assigned to a AddressObjectGroup."""

    address = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    address_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.CASCADE)


class DestAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination Address if assigned to a PolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination AddressGroup if assigned to a PolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class FQDNIPAddressM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated IPAddress if assigned to a FQDN."""

    fqdn = models.ForeignKey("nautobot_firewall_models.FQDN", on_delete=models.CASCADE)
    ip_address = models.ForeignKey("ipam.IPAddress", on_delete=models.PROTECT)


class PolicyDeviceM2M(BaseModel):
    """Through model to add weight to the the Policy & Device relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.CASCADE)
    device = models.ForeignKey("dcim.Device", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "device"]


class PolicyDynamicGroupM2M(BaseModel):
    """Through model to add weight to the the Policy & DynamicGroup relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.CASCADE)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "dynamic_group"]


class PolicyRuleM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated PolicyRule if assigned to a Policy."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.CASCADE)
    rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.PROTECT)


class ServiceObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated ServiceGroup if assigned to a PolicyRule."""

    service = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    service_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.CASCADE)


class SrcAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated source Address if assigned to a PolicyRule."""

    addr = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class SrcAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated source AddressGroup if assigned to a PolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class SrcUserM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated User if assigned to a PolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class SrcUserGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated UserGroup if assigned to a PolicyRule."""

    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class SrcSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated Service if assigned to a PolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class SrcSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated ServiceGroup if assigned to a PolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated Service if assigned to a PolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated ServiceGroup if assigned to a PolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class UserObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated User if assigned to a UserGroup."""

    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.CASCADE)


class ZoneInterfaceM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated Interface if assigned to a Zone."""

    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.CASCADE)
    interface = models.ForeignKey("dcim.Interface", on_delete=models.PROTECT)


class ZoneVRFM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated VRF if assigned to a Zone."""

    zone = models.ForeignKey("nautobot_firewall_models.Zone", on_delete=models.CASCADE)
    vrf = models.ForeignKey("ipam.vrf", on_delete=models.PROTECT)
