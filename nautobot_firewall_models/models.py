"""Models for the Firewall plugin."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.template.defaultfilters import slugify
from django.urls import reverse
from nautobot.core.models.generics import PrimaryModel, BaseModel
from nautobot.extras.models import StatusField, Status
from nautobot.extras.models.tags import TaggedItem
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from netaddr import IPAddress
from taggit.managers import TaggableManager

from nautobot_firewall_models import choices, validators


def get_default_status():
    """Returns a default status value basedo n plugin config."""
    status_name = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {}).get("status_name", "Active")
    return Status.objects.get(name=status_name)


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
    # pylint: disable=R0901
    """IPRange model to track ranges of IPs in firewall rules."""

    start_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="IPv4 or IPv6 host address",
    )
    end_address = VarbinaryIPField(
        null=False,
        db_index=True,
        help_text="IPv4 or IPv6 host address",
    )
    vrf = models.ForeignKey(
        to="ipam.VRF", on_delete=models.CASCADE, related_name="ip_ranges", blank=True, null=True, verbose_name="VRF"
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
    # pylint: disable=R0901
    """FQDN model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    ip_addresses = models.ManyToManyField(to="ipam.IPAddress", blank=True, related_name="fqdns")
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
    # pylint: disable=R0901
    """FQDN model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    fqdn = models.ForeignKey(to=FQDN, on_delete=models.CASCADE, null=True, blank=True)
    ip_range = models.ForeignKey(to=IPRange, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.ForeignKey(to="ipam.IPAddress", on_delete=models.CASCADE, null=True, blank=True)
    prefix = models.ForeignKey(to="ipam.Prefix", on_delete=models.CASCADE, null=True, blank=True)
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
    # pylint: disable=R0901
    """AddressObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(to=AddressObject, blank=True, related_name="address_object_groups")
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
class AddressPolicyObject(PrimaryModel):
    # pylint: disable=R0901
    """AddressPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(to=AddressObject, blank=True, related_name="address_policy_objects")
    address_object_groups = models.ManyToManyField(
        to=AddressObjectGroup, blank=True, related_name="address_policy_objects"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Address Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:addresspolicyobject", args=[self.pk])

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
    # pylint: disable=R0901
    """UserObject model."""

    username = models.CharField(
        max_length=50,
        unique=True,
    )
    name = models.CharField(max_length=50, blank=True)
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
    # pylint: disable=R0901
    """UserObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(to=UserObject, blank=True, related_name="user_object_groups")
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
class UserPolicyObject(PrimaryModel):
    # pylint: disable=R0901
    """UserPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(to=UserObject, blank=True, related_name="user_policy_objects")
    user_object_groups = models.ManyToManyField(to=UserObjectGroup, blank=True, related_name="user_policy_objects")
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "User Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:userpolicyobject", args=[self.pk])

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
    # pylint: disable=R0901
    """Zone model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    vrfs = models.ManyToManyField(to="ipam.VRF", blank=True, related_name="zones")
    interfaces = models.ManyToManyField(to="dcim.Interface", blank=True, related_name="zones")
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
    # pylint: disable=R0901
    """ServiceObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    port = models.CharField(null=True, blank=True, validators=[validators.validate_port], max_length=20)
    ip_protocol = models.CharField(choices=choices.IP_PROTOCOL_CHOICES, max_length=20)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Objects"
        unique_together = ["slug", "port", "ip_protocol"]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:serviceobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.ip_protocol:
            return f"{self.slug}:{self.port}:{self.ip_protocol}"
        return f"{self.slug}:{self.port}"

    def save(self, *args, **kwargs):
        """Overloads to enforce use of slugify."""
        self.slug = slugify(self.name)
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
    # pylint: disable=R0901
    """ServiceGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(to=ServiceObject, blank=True, related_name="service_object_groups")
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
class ServicePolicyObject(PrimaryModel):
    # pylint: disable=R0901
    """ServicePolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject,
        blank=True,
        related_name="service_policy_objects",
    )
    service_object_groups = models.ManyToManyField(
        to=ServiceObjectGroup,
        blank=True,
        related_name="service_policy_objects",
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Policy Objects"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:servicepolicyobject", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


class SourceDestination(PrimaryModel):
    # pylint: disable=R0901
    """Source model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    address = models.ForeignKey(to=AddressPolicyObject, on_delete=models.CASCADE)
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE, null=True, blank=True)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        abstract = True


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
class Source(SourceDestination):
    # pylint: disable=R0901
    """Source model."""

    user = models.ForeignKey(to=UserPolicyObject, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        """Meta class."""

        ordering = ["description"]
        verbose_name_plural = "Sources"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:source", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.user:
            return f"{self.address} - {self.user} - {self.zone}"
        return f"{self.address} - {self.zone}"


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
class Destination(SourceDestination):
    # pylint: disable=R0901
    """Destination model."""

    class Meta:
        """Meta class."""

        ordering = ["description"]
        verbose_name_plural = "Destinations"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:destination", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.address} - {self.zone}"


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
    # pylint: disable=R0901
    """PolicyRule model."""

    name = models.CharField(max_length=50, blank=True, null=True)
    tags = TaggableManager(through=TaggedItem)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE, related_name="policy_rules")
    service = models.ForeignKey(
        to=ServicePolicyObject, on_delete=models.CASCADE, null=True, related_name="policy_rules"
    )
    destination = models.ForeignKey(to=Destination, on_delete=models.CASCADE, related_name="policy_rules")
    action = models.CharField(choices=choices.ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

    class Meta:
        """Meta class."""

        verbose_name_plural = "Policy Rules"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:policyrule", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.name:
            return self.name
        return f"{self.source} - {self.destination} - {self.action}"


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
    # pylint: disable=R0901
    """Policy model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    policy_rules = models.ManyToManyField(to=PolicyRule, through="PolicyRuleM2M", related_name="policies")
    devices = models.ManyToManyField(to="dcim.Device", through="PolicyDeviceM2M", related_name="firewall_policies")
    dynamic_groups = models.ManyToManyField(
        to="extras.DynamicGroup", through="PolicyDynamicGroupM2M", related_name="firewall_policies"
    )
    status = StatusField(
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_related",  # e.g. dcim_device_related
        default=get_default_status,
    )

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


class PolicyRuleM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & PolicyRule relationship."""

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    rule = models.ForeignKey(PolicyRule, on_delete=models.CASCADE)
    index = models.PositiveSmallIntegerField(null=True)

    class Meta:
        """Meta class."""

        ordering = ["index"]
        constraints = [
            UniqueConstraint(fields=["policy", "rule", "index"], name="unique_with_index"),
            UniqueConstraint(fields=["policy", "rule"], name="unique_without_index", condition=Q(index=None)),
        ]


class PolicyDeviceM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & Device relationship."""

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    device = models.ForeignKey("dcim.Device", on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "device"]


class PolicyDynamicGroupM2M(BaseModel):
    # pylint: disable=R0901
    """Through model to add index to the the Policy & DynamicGroup relationship."""

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    dynamic_group = models.ForeignKey("extras.DynamicGroup", on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=100)

    class Meta:
        """Meta class."""

        ordering = ["weight"]
        unique_together = ["policy", "dynamic_group"]
