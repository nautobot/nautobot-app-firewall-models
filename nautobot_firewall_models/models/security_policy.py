"""Models for the Firewall app."""
# pylint: disable=duplicate-code, too-many-lines

from django.db import models
from nautobot.core.models.generics import BaseModel, PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

from nautobot_firewall_models import choices
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
class PolicyRule(PrimaryModel):
    """
    A PolicyRule is a the equivalent of a single in a firewall policy or access list.

    Firewall policies are typically made up of several individual rules.
    """

    name = models.CharField(max_length=100)
    source_users = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.UserObject", related_name="policy_rules"
    )
    source_user_groups = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.UserObjectGroup", related_name="policy_rules"
    )
    source_addresses = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.AddressObject", related_name="source_policy_rules"
    )
    source_address_groups = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.AddressObjectGroup", related_name="source_policy_rules"
    )
    source_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_policy_rules",
    )
    source_services = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.ServiceObject", related_name="source_policy_rules"
    )
    source_service_groups = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.ServiceObjectGroup", related_name="source_policy_rules"
    )
    destination_addresses = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.AddressObject", related_name="destination_policy_rules"
    )
    destination_address_groups = models.ManyToManyField(
        blank=True,
        to="nautobot_firewall_models.AddressObjectGroup",
        related_name="destination_policy_rules",
    )
    destination_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="destination_policy_rules",
    )
    destination_services = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.ServiceObject", related_name="destination_policy_rules"
    )
    destination_service_groups = models.ManyToManyField(
        blank=True,
        to="nautobot_firewall_models.ServiceObjectGroup",
        related_name="destination_policy_rules",
    )
    action = models.CharField(choices=choices.ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    applications = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.ApplicationObject", related_name="policy_rules"
    )
    application_groups = models.ManyToManyField(
        blank=True, to="nautobot_firewall_models.ApplicationObjectGroup", related_name="policy_rules"
    )
    request_id = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    index = models.PositiveSmallIntegerField(null=True, blank=True)

    clone_fields = [
        "source_users",
        "source_user_groups",
        "source_addresses",
        "source_address_groups",
        "source_zone",
        "source_services",
        "source_service_groups",
        "destination_addresses",
        "destination_address_groups",
        "destination_zone",
        "destination_services",
        "destination_service_groups",
        "action",
        "log",
        "status",
    ]
    natural_key_field_names = ["pk"]

    class Meta:
        """Meta class."""

        ordering = ["index", "name"]
        verbose_name_plural = "Policy Rules"

    def rule_details(self):
        """Convience method to convert to more consumable dictionary."""
        row = {}
        row["rule"] = self
        row["source_address_groups"] = self.source_address_groups.all()
        row["source_addresses"] = self.source_addresses.all()
        row["source_users"] = self.source_users.all()
        row["source_user_groupes"] = self.source_user_groups.all()
        row["source_zone"] = self.source_zone
        row["source_services"] = self.source_services.all()
        row["source_service_groups"] = self.source_service_groups.all()

        row["destination_address_groups"] = self.destination_address_groups.all()
        row["destination_addresses"] = self.destination_addresses.all()
        row["destination_zone"] = self.destination_zone
        row["destination_services"] = self.destination_services.all()
        row["destination_service_groups"] = self.destination_service_groups.all()

        row["action"] = self.action
        row["log"] = self.log
        row["status"] = self.status
        row["request_id"] = self.request_id
        return row

    def to_json(self):
        """Convience method to convert to json."""
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
class Policy(PrimaryModel):
    """
    The overarching model that is the full firewall policy with all underlying rules and child objects.

    Each Policy can be assigned to both devices and to dynamic groups which in turn can assign the policy to a related device.
    """

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    policy_rules = models.ManyToManyField(to=PolicyRule, blank=True, related_name="policies")
    assigned_devices = models.ManyToManyField(
        to="dcim.Device", through="PolicyDeviceM2M", related_name="firewall_policies"
    )
    assigned_dynamic_groups = models.ManyToManyField(
        to="extras.DynamicGroup", through="PolicyDynamicGroupM2M", related_name="firewall_policies"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    tenant = models.ForeignKey(
        to="tenancy.Tenant",
        on_delete=models.PROTECT,
        related_name="policies",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Policies"

    @property
    def policy_details(self):
        """Convience method to convert to a Python list of dictionaries."""
        data = []
        for policy_rule in self.policy_rules.all():
            data.append(policy_rule.rule_details())
        return data

    def to_json(self):
        """Convience method to convert to json."""
        return model_to_json(self, "nautobot_firewall_models.api.serializers.PolicySerializer")

    def __str__(self):
        """Stringify instance."""
        return self.name


###########################
# Through Models
###########################


class PolicyDeviceM2M(BaseModel):
    """Through model to add weight to the the Policy & Device relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.CASCADE)
    device = models.ForeignKey("dcim.Device", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "device"]

    def __str__(self):
        """Stringify instance."""
        return f"{self.policy.name} - {self.device.name} - {self.weight}"


class PolicyDynamicGroupM2M(BaseModel):
    """Through model to add weight to the the Policy & DynamicGroup relationship."""

    policy = models.ForeignKey("nautobot_firewall_models.Policy", on_delete=models.CASCADE)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.PROTECT)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "dynamic_group"]

    def __str__(self):
        """Stringify instance."""
        return f"{self.policy.name} - {self.dynamic_group.name} - {self.weight}"
