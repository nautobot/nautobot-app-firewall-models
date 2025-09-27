"""Models for the Firewall app."""
# pylint: disable=duplicate-code, too-many-lines

from django.db import models
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
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
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH)
    remark = models.BooleanField(default=False)
    log = models.BooleanField(default=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    request_id = models.CharField(max_length=CHARFIELD_MAX_LENGTH, blank=True, verbose_name="Request ID")
    description = models.CharField(max_length=1024, blank=True)
    index = models.PositiveSmallIntegerField(null=True, blank=True)

    # Data that can not undergo a translation
    source_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_nat_policy_rules",
        verbose_name="Source Zone",
    )
    destination_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="destination_nat_policy_rules",
        verbose_name="Destination Zone",
    )

    # Original source data
    original_source_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        blank=True,
        related_name="original_source_nat_policy_rules",
        verbose_name="Original Source Addresses",
    )
    original_source_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        blank=True,
        related_name="original_source_nat_policy_rules",
        verbose_name="Original Source Address Groups",
    )
    original_source_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        blank=True,
        related_name="original_source_nat_policy_rules",
        verbose_name="Original Source Services",
    )
    original_source_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        blank=True,
        related_name="original_source_nat_policy_rules",
        verbose_name="Original Source Service Groups",
    )

    # Translated source data
    translated_source_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        blank=True,
        related_name="translated_source_nat_policy_rules",
        verbose_name="Translated Source Addresses",
    )
    translated_source_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        blank=True,
        related_name="translated_source_nat_policy_rules",
        verbose_name="Translated Source Address Groups",
    )
    translated_source_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        blank=True,
        related_name="translated_source_nat_policy_rules",
        verbose_name="Translated Source Services",
    )
    translated_source_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        blank=True,
        related_name="translated_source_nat_policy_rules",
        verbose_name="Translated Source Service Groups",
    )

    # Original destination data
    original_destination_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        blank=True,
        related_name="original_destination_nat_policy_rules",
        verbose_name="Original Destination Addresses",
    )
    original_destination_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        blank=True,
        related_name="original_destination_nat_policy_rules",
        verbose_name="Original Destination Address Groups",
    )
    original_destination_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        blank=True,
        related_name="original_destination_nat_policy_rules",
        verbose_name="Original Destination Services",
    )
    original_destination_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        blank=True,
        related_name="original_destination_nat_policy_rules",
        verbose_name="Original Destination Service Groups",
    )

    # Translated destination data
    translated_destination_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject",
        blank=True,
        related_name="translated_destination_nat_policy_rules",
        verbose_name="Translated Destination Addresses",
    )
    translated_destination_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        blank=True,
        related_name="translated_destination_nat_policy_rules",
        verbose_name="Translated Destination Address Groups",
    )
    translated_destination_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject",
        blank=True,
        related_name="translated_destination_nat_policy_rules",
        verbose_name="Translated Destination Services",
    )
    translated_destination_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        blank=True,
        related_name="translated_destination_nat_policy_rules",
        verbose_name="Translated Destination Service Groups",
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
        max_length=1024,
        blank=True,
    )
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    nat_policy_rules = models.ManyToManyField(
        to="nautobot_firewall_models.NATPolicyRule",
        blank=True,
        related_name="nat_policies",
        verbose_name="NAT Policy Rules",
    )
    assigned_devices = models.ManyToManyField(
        to="dcim.Device",
        through="NATPolicyDeviceM2M",
        related_name="nat_policies",
        blank=True,
        verbose_name="Assigned Devices",
    )
    assigned_dynamic_groups = models.ManyToManyField(
        to="extras.DynamicGroup",
        through="NATPolicyDynamicGroupM2M",
        related_name="nat_policies",
        blank=True,
        verbose_name="Assigned Dynamic Groups",
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


class NATPolicyDeviceM2M(BaseModel):
    """Through model to add weight to the NATPolicy & Device relationship."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    device = models.ForeignKey("dcim.Device", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["nat_policy", "device"]

    def __str__(self):
        """Stringify instance."""
        return f"{self.nat_policy.name} - {self.device.name} - {self.weight}"


class NATPolicyDynamicGroupM2M(BaseModel):
    """Through model to add weight to the NATPolicy & DynamicGroup relationship."""

    nat_policy = models.ForeignKey("nautobot_firewall_models.NATPolicy", on_delete=models.CASCADE)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.PROTECT, verbose_name="Dynamic Group")
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["nat_policy", "dynamic_group"]

    def __str__(self):
        """Stringify instance."""
        return f"{self.nat_policy.name} - {self.dynamic_group.name} - {self.weight}"
