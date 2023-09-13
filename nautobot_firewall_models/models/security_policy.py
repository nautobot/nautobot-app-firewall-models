"""Models for the Firewall plugin."""
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
        to="nautobot_firewall_models.UserObject", through="SrcUserM2M", related_name="policy_rules"
    )
    source_user_groups = models.ManyToManyField(
        to="nautobot_firewall_models.UserObjectGroup", through="SrcUserGroupM2M", related_name="policy_rules"
    )
    source_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject", through="SrcAddrM2M", related_name="source_policy_rules"
    )
    source_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup", through="SrcAddrGroupM2M", related_name="source_policy_rules"
    )
    source_zone = models.ForeignKey(
        to="nautobot_firewall_models.Zone",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="source_policy_rules",
    )
    source_services = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObject", through="SrcSvcM2M", related_name="source_policy_rules"
    )
    source_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup", through="SrcSvcGroupM2M", related_name="source_policy_rules"
    )
    destination_addresses = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObject", through="DestAddrM2M", related_name="destination_policy_rules"
    )
    destination_address_groups = models.ManyToManyField(
        to="nautobot_firewall_models.AddressObjectGroup",
        through="DestAddrGroupM2M",
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
        to="nautobot_firewall_models.ServiceObject", through="DestSvcM2M", related_name="destination_policy_rules"
    )
    destination_service_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ServiceObjectGroup",
        through="DestSvcGroupM2M",
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
        to="nautobot_firewall_models.ApplicationObject", through="ApplicationM2M", related_name="policy_rules"
    )
    application_groups = models.ManyToManyField(
        to="nautobot_firewall_models.ApplicationObjectGroup", through="ApplicationGroupM2M", related_name="policy_rules"
    )
    request_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
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
    policy_rules = models.ManyToManyField(to=PolicyRule, through="PolicyRuleM2M", related_name="policies")
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


class ApplicationM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination ApplicationObject if assigned to a PolicyRule."""

    app = models.ForeignKey("nautobot_firewall_models.ApplicationObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class ApplicationGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination ApplicationObjectGroup if assigned to a PolicyRule."""

    app_group = models.ForeignKey("nautobot_firewall_models.ApplicationObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestAddrGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination Address if assigned to a PolicyRule."""

    addr_group = models.ForeignKey("nautobot_firewall_models.AddressObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestAddrM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated destination AddressGroup if assigned to a PolicyRule."""

    user = models.ForeignKey("nautobot_firewall_models.AddressObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestSvcM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated Service if assigned to a PolicyRule."""

    svc = models.ForeignKey("nautobot_firewall_models.ServiceObject", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


class DestSvcGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated ServiceGroup if assigned to a PolicyRule."""

    svc_group = models.ForeignKey("nautobot_firewall_models.ServiceObjectGroup", on_delete=models.PROTECT)
    pol_rule = models.ForeignKey("nautobot_firewall_models.PolicyRule", on_delete=models.CASCADE)


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

    class Meta:
        """Meta class."""

        ordering = ["rule__index"]


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
