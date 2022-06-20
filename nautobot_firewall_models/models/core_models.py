"""Models for the Firewall plugin."""
import json

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

from nautobot.core.models.generics import PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.models.tags import TaggedItem
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from nautobot.utilities.utils import serialize_object_v2
from netaddr import IPAddress
from taggit.managers import TaggableManager

from nautobot_firewall_models import choices, validators
from nautobot_firewall_models.utils import get_default_status, model_to_json


def get_single_attr(obj, attrs):
    for attr in attrs:
        if getattr(obj, attr) is not None:
            return attr
    else:
        raise ValueError(f"The object {obj} did not have any of the attrs {attrs}")


def list_expander(length):
    return [None] * length


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
class IPRange(PrimaryModel):
    """IPRange model to track ranges of IPs in firewall rules."""

    start_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="Starting IPv4 or IPv6 host address",
    )
    end_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="Ending IPv4 or IPv6 host address",
    )
    vrf = models.ForeignKey(
        to="ipam.VRF", on_delete=models.PROTECT, related_name="ip_ranges", blank=True, null=True, verbose_name="VRF"
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    size = models.PositiveIntegerField(editable=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["start_address"]
        verbose_name_plural = "IP Ranges"
        constraints = [
            UniqueConstraint(fields=["start_address", "end_address", "vrf"], name="unique_with_vrf"),
            UniqueConstraint(fields=["start_address", "end_address"], condition=Q(vrf=None), name="unique_without_vrf"),
        ]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:iprange", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.start_address}-{self.end_address}"

    def save(self, *args, **kwargs):
        """Overloads to inject size attr."""
        # Record the range's size (number of IP addresses)
        self.clean()
        self.size = int(IPAddress(self.end_address) - IPAddress(self.start_address)) + 1
        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Overloads to validate attr for form verification."""
        if not getattr(self, "start_address") or not getattr(self, "end_address"):
            raise ValidationError("Must have `start_address` and `end_address`.")
        if IPAddress(self.start_address) > IPAddress(self.end_address):
            raise ValidationError("`end_address` must be >= than `start_address`.")

        super().clean(*args, **kwargs)


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
class FQDN(PrimaryModel):
    """Models fully qualified domain names, can be used on some firewall in place of a static IP."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(
        max_length=254, unique=True, help_text="Resolvable fully qualified domain name (i.e. networktocode.com)"
    )
    ip_addresses = models.ManyToManyField(
        to="ipam.IPAddress",
        blank=True,
        through="FQDNIPAddressM2M",
        related_name="fqdns",
        help_text="IP(s) an FQDN should resolve to.",
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name = "FQDN"
        verbose_name_plural = "FQDNs"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:fqdn", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


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
class AddressObject(PrimaryModel):
    """Intermediate model to aggregate underlying address items, to allow for easier management."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True, help_text="Name descriptor for an address object type.")
    fqdn = models.ForeignKey(to=FQDN, on_delete=models.PROTECT, null=True, blank=True)
    ip_range = models.ForeignKey(to=IPRange, on_delete=models.PROTECT, null=True, blank=True)
    ip_address = models.ForeignKey(to="ipam.IPAddress", on_delete=models.PROTECT, null=True, blank=True)
    prefix = models.ForeignKey(to="ipam.Prefix", on_delete=models.PROTECT, null=True, blank=True)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:addressobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name

    def save(self, *args, **kwargs):
        """Overloads to enforce clear."""
        self.clean()
        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Overloads to validate attr for form verification."""
        address_types = ["fqdn", "ip_range", "ip_address", "prefix"]
        address_count = 0
        for i in address_types:
            if hasattr(self, i) and getattr(self, i) is not None:
                address_count += 1
        if address_count != 1:
            raise ValidationError(f"Must specify only one address from type {address_types}, {address_count} found.")

        super().clean(*args, **kwargs)

    @property
    def address(self):  # pylint: disable=inconsistent-return-statements
        """Returns the assigned address object."""
        for i in ["fqdn", "ip_range", "ip_address", "prefix"]:
            if getattr(self, i):
                return getattr(self, i)


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
class AddressObjectGroup(PrimaryModel):
    """Groups together AddressObjects to better mimic grouping sets of address objects that have a some commonality."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True, help_text="Name descriptor for a group address objects.")
    address_objects = models.ManyToManyField(
        to=AddressObject, blank=True, through="AddressObjectGroupM2M", related_name="address_object_groups"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:addressobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


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
class UserObject(PrimaryModel):
    """Source users can be used to identify the origin of traffic for a user on some firewalls."""

    username = models.CharField(
        max_length=100, unique=True, help_text="Signifies the username in identify provider (i.e. john.smith)"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Signifies the name of the user, commonly first & last name (i.e. John Smith)",
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["username"]
        verbose_name_plural = "User Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:userobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.username


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
class UserObjectGroup(PrimaryModel):
    """Grouping of individual user objects, does NOT have any relationship to AD groups or any other IDP group."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    user_objects = models.ManyToManyField(
        to=UserObject, blank=True, through="UserObjectGroupM2M", related_name="user_object_groups"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "User Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:userobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


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
class Zone(PrimaryModel):
    """Zones common on firewalls and are typically seen as representations of area (i.e. DMZ trust untrust)."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True, help_text="Name of the zone (i.e. trust)")
    vrfs = models.ManyToManyField(to="ipam.VRF", blank=True, through="ZoneVRFM2M", related_name="zones")
    interfaces = models.ManyToManyField(
        to="dcim.Interface", blank=True, through="ZoneInterfaceM2M", related_name="zones"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:zone", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


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
class ServiceObject(PrimaryModel):
    """ServiceObject matches a IANA IP Protocol with a name and optional port number (i.e. TCP HTTPS 443)."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, help_text="Name of the service (i.e. HTTP)")
    port = models.CharField(
        null=True,
        blank=True,
        validators=[validators.validate_port],
        max_length=20,
        help_text="The port or port range to tie to a service (i.e. HTTP would be port 80)",
    )
    ip_protocol = models.CharField(
        choices=choices.IP_PROTOCOL_CHOICES, max_length=20, help_text="IANA IP Protocol (i.e. TCP UDP ICMP)"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Objects"
        unique_together = ["port", "ip_protocol"]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:serviceobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name

    def save(self, *args, **kwargs):
        """Overload save to call full_clean to ensure validators run."""
        self.full_clean()
        super().save(*args, **kwargs)


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
class ServiceObjectGroup(PrimaryModel):
    """Groups service objects."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject, blank=True, through="ServiceObjectGroupM2M", related_name="service_object_groups"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Object Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:serviceobjectgroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


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
    tags = TaggableManager(through=TaggedItem)
    source_user = models.ManyToManyField(to=UserObject, through="SrcUserM2M", related_name="policy_rules")
    source_user_group = models.ManyToManyField(
        to=UserObjectGroup, through="SrcUserGroupM2M", related_name="policy_rules"
    )
    source_address = models.ManyToManyField(to=AddressObject, through="SrcAddrM2M", related_name="source_policy_rules")
    source_address_group = models.ManyToManyField(
        to=AddressObjectGroup, through="SrcAddrGroupM2M", related_name="source_policy_rules"
    )
    source_zone = models.ForeignKey(
        to=Zone, null=True, blank=True, on_delete=models.SET_NULL, related_name="source_policy_rules"
    )
    destination_address = models.ManyToManyField(
        to=AddressObject, through="DestAddrM2M", related_name="destination_policy_rules"
    )
    destination_address_group = models.ManyToManyField(
        to=AddressObjectGroup, through="DestAddrGroupM2M", related_name="destination_policy_rules"
    )
    destination_zone = models.ForeignKey(
        to=Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name="destination_policy_rules"
    )
    service = models.ManyToManyField(to=ServiceObject, through="SvcM2M", related_name="policy_rules")
    service_group = models.ManyToManyField(to=ServiceObjectGroup, through="SvcGroupM2M", related_name="policy_rules")
    action = models.CharField(choices=choices.ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )
    request_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Policy Rules"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:policyrule", args=[self.pk])

    def rule_details(self):
        row = {}
        row["rule"] = self
        row["source_address_group"] = self.source_address_group.all()
        row["source_address"] = self.source_address.all()
        row["source_user"] = self.source_user.all()
        row["source_user_group"] = self.source_user_group.all()
        row["source_zone"] = self.source_zone

        row["destination_address_group"] = self.destination_address_group.all()
        row["destination_address"] = self.destination_address.all()
        row["destination_zone"] = self.destination_zone

        row["service"] = self.service.all()
        row["service_group"] = self.service_group.all()

        row["action"] = self.action
        row["log"] = self.log
        row["status"] = self.status
        row["request_id"] = self.request_id
        return row

    def to_json(self):
        return json.loads(JSONRenderer().render(serialize_object_v2(self)))

    def __str__(self):
        """Stringify instance."""
        if self.request_id:
            return f"{self.name} - {self.request_id}"
        return self.name


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

    def policy_details(self):
        data = []
        for policy_rule in self.policy_rules.all():
            data.append(policy_rule.rule_details())
        return data

    def to_json(self):
        return json.loads(JSONRenderer().render(serialize_object_v2(self)))

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Policies"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:policy", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name
