"""Models for the Firewall plugin."""
# pylint: disable=duplicate-code, too-many-lines

from django.db import models
from nautobot.core.models.generics import BaseModel, PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

from nautobot_firewall_models.utils import get_default_status, model_to_json


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
class NATPolicyRule(PrimaryModel):
    """
    A NATPolicyRule is the equivalent of a single rule in a NAT policy or access list.

    NAT policies are typically made up of several individual rules.
    """

    # Metadata
    name = models.CharField(max_length=100)
    remark = models.BooleanField(default=False)
    log = models.BooleanField(default=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    request_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    index = models.PositiveSmallIntegerField(null=True, blank=True)

    # Data that can not undergo a translation
    source_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_nat_policy_rules",
    )
    destination_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="destination_nat_policy_rules",
    )

    # Original source data
    original_source_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        through="NATOrigSrcAddrM2M",
        related_name="original_source_nat_policy_rules",
    )
    original_source_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        through="NATOrigSrcAddrGroupM2M",
        related_name="original_source_nat_policy_rules",
    )
    original_source_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        through="NATOrigSrcSvcM2M",
        related_name="original_source_nat_policy_rules",
    )
    original_source_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        through="NATOrigSrcSvcGroupM2M",
        related_name="original_source_nat_policy_rules",
    )

    # Translated source data
    translated_source_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        through="NATTransSrcAddrM2M",
        related_name="translated_source_nat_policy_rules",
    )
    translated_source_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        through="NATTransSrcAddrGroupM2M",
        related_name="translated_source_nat_policy_rules",
    )
    translated_source_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        through="NATTransSrcSvcM2M",
        related_name="translated_source_nat_policy_rules",
    )
    translated_source_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        through="NATTransSrcSvcGroupM2M",
        related_name="translated_source_nat_policy_rules",
    )

    # Original destination data
    original_destination_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        through="NATOrigDestAddrM2M",
        related_name="original_destination_nat_policy_rules",
    )
    original_destination_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        through="NATOrigDestAddrGroupM2M",
        related_name="original_destination_nat_policy_rules",
    )
    original_destination_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        through="NATOrigDestSvcM2M",
        related_name="original_destination_nat_policy_rules",
    )
    original_destination_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        through="NATOrigDestSvcGroupM2M",
        related_name="original_destination_nat_policy_rules",
    )

    # Translated destination data
    translated_destination_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        through="NATTransDestAddrM2M",
        related_name="translated_destination_nat_policy_rules",
    )
    translated_destination_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        through="NATTransDestAddrGroupM2M",
        related_name="translated_destination_nat_policy_rules",
    )
    translated_destination_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        through="NATTransDestSvcM2M",
        related_name="translated_destination_nat_policy_rules",
    )
    translated_destination_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        through="NATTransDestSvcGroupM2M",
        related_name="translated_destination_nat_policy_rules",
    )

    clone_fields = [
        "destination_zone",
        "source_zone",
        "original_source_addresses",
        "original_source_address_groups",
        "original_source_services",
        "original_source_service_groups",
        "original_destination_addresses",
        "original_destination_address_groups",
        "original_destination_services",
        "original_destination_service_groups",
        "translated_source_addresses",
        "translated_source_address_groups",
        "translated_source_services",
        "translated_source_service_groups",
        "translated_destination_addresses",
        "translated_destination_address_groups",
        "translated_destination_services",
        "translated_destination_service_groups",
        "remark",
        "log",
        "status",
    ]

    natural_key_field_names = ["pk"]

    class Meta:
        """Meta class."""

        ordering = ["index"]
        verbose_name = "NAT Policy Rule"
        verbose_name_plural = "NAT Policy Rules"

    def rule_details(self):
        """Convenience method to convert to more consumable dictionary."""
        row = {}
        row["rule"] = self
        row["source_zone"] = self.source_zone
        row["destination_zone"] = self.destination_zone

        row["original_source_address_groups"] = self.original_source_address_groups.all()
        row["original_source_addresses"] = self.original_source_addresses.all()
        row["original_source_services"] = self.original_source_services.all()
        row["original_source_service_groups"] = self.original_source_service_groups.all()

        row["translated_source_address_groups"] = self.translated_source_address_groups.all()
        row["translated_source_addresses"] = self.translated_source_addresses.all()
        row["translated_source_services"] = self.translated_source_services.all()
        row["translated_source_service_groups"] = self.translated_source_service_groups.all()

        row["original_destination_address_groups"] = self.original_destination_address_groups.all()
        row["original_destination_addresses"] = self.original_destination_addresses.all()
        row["original_destination_services"] = self.original_destination_services.all()
        row["original_destination_service_groups"] = self.original_destination_service_groups.all()

        row["translated_destination_address_groups"] = self.translated_destination_address_groups.all()
        row["translated_destination_addresses"] = self.translated_destination_addresses.all()
        row["translated_destination_services"] = self.translated_destination_services.all()
        row["translated_destination_service_groups"] = self.translated_destination_service_groups.all()

        row["remark"] = self.remark
        row["log"] = self.log
        row["status"] = self.status
        row["request_id"] = self.request_id
        return row

    def to_json(self):
        """Convenience method to convert to json."""
        return model_to_json(self)

    def __str__(self):
        """Stringify instance."""
        if self.request_id and self.name:
            return f"{self.name} - {self.request_id}"
        if self.name:
            return self.name
        return str(self.id)


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
class NATPolicy(PrimaryModel):
    """
    The overarching model that is the full NAT policy with all underlying rules and child objects.

    Each NATPolicy can be assigned to both devices and to dynamic groups which in turn can assign the policy to a related device.
    """

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    nat_policy_rules = models.ManyToManyField(to=NATPolicyRule, through="NATPolicyRuleM2M", related_name="nat_policies")
    assigned_devices = models.ManyToManyField(
        to="dcim.Device", through="NATPolicyDeviceM2M", related_name="nat_policies"
    )
    assigned_dynamic_groups = models.ManyToManyField(
        to="extras.DynamicGroup", through="NATPolicyDynamicGroupM2M", related_name="nat_policies"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="nat_policies",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name = "NAT Policy"
        verbose_name_plural = "NAT Policies"

    @property
    def policy_details(self):
        """Convenience method to convert to a Python list of dictionaries."""
        return [rule.rule_details() for rule in self.nat_policy_rules.all()]

    def to_json(self):
        """Convenience method to convert to json."""
        return model_to_json(self)

    def __str__(self):
        """Stringify instance."""
        return self.name


###########################
# Through Models
###########################


class NATOrigDestAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original destination AddressObject if assigned to a NATPolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigDestAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original destination AddressObjectGroup if assigned to a NATPolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigDestSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original destination ServiceObjectGroup if assigned to a NATPolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigDestSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original destination ServiceObject if assigned to a NATPolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigSrcAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original source AddressObjectGroup if assigned to a NATPolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigSrcAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original source AddressObject if assigned to a NATPolicyRule."""

    addr = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigSrcSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original source ServiceObjectGroup if assigned to a NATPolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATOrigSrcSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated original source ServiceObject if assigned to a NATPolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATPolicyDeviceM2M(BaseModel):
    """Through model to add weight to the NATPolicy & Device relationship."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    device = models.ForeignKey("dcim.Device", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["nat_policy", "device"]


class NATPolicyDynamicGroupM2M(BaseModel):
    """Through model to add weight to the NATPolicy & DynamicGroup relationship."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["nat_policy", "dynamic_group"]


class NATPolicyNATRuleM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated NATPolicyRule if assigned to a NATPolicy."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    nat_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.PROTECT)


class NATPolicyRuleM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated NATPolicyRule if assigned to a NATPolicy."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    nat_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.PROTECT)


class NATSrcUserGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated UserGroup if assigned to a NATPolicyRule."""

    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATSrcUserM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated User if assigned to a NATPolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransDestAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated destination AddressObjectGroup if assigned to a NATPolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransDestAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated destination AddressObject if assigned to a NATPolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransDestSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated destination ServiceObjectGroup if assigned to a NATPolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransDestSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated destination ServiceObject if assigned to a NATPolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransSrcAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated source AddressObjectGroup if assigned to a NATPolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransSrcAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated source AddressObject if assigned to a NATPolicyRule."""

    addr = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransSrcSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated source ServiceObjectGroup if assigned to a NATPolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)


class NATTransSrcSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated translated source ServiceObject if assigned to a NATPolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    nat_pol_rule = models.ForeignKey("nautobot_firewall_models.NATPolicyRule", on_delete=models.CASCADE)
