"""Models for the Firewall plugin."""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.template.defaultfilters import slugify
from django.urls import reverse
from nautobot.core.models.generics import OrganizationalModel, PrimaryModel
from nautobot.extras.models import StatusModel
from nautobot.extras.models.tags import TaggedItem
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from netaddr import IPAddress
from taggit.managers import TaggableManager

from nautobot_firewall_models import choices


@extras_features(
    "custom_fields",
    "custom_validators",
    "graphql",
    "relationships",
)
class Role(OrganizationalModel):
    """A Role represents the functional role of objects inside the Firewall model plugin.

    This Model is a copy of `nautobot.ipam.models.Role`, it is meant to be deprecated once
    `nautobot.extras.models.Role` is implemented
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    weight = models.PositiveSmallIntegerField(default=1000)
    description = models.CharField(
        max_length=200,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["weight", "name"]

    def __str__(self):
        """Stringify instance."""
        return self.name

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:role", args=[self.pk])


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
class IPRange(PrimaryModel, StatusModel):
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
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class FQDN(PrimaryModel, StatusModel):
    """FQDN model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    ip_addresses = models.ManyToManyField(to="ipam.IPAddress", blank=True)
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        """Meta class."""

        ordering = ["name"]
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
class AddressObject(PrimaryModel, StatusModel):
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
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class AddressObjectGroup(PrimaryModel, StatusModel):
    """AddressObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(
        to=AddressObject,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class AddressPolicyObject(PrimaryModel, StatusModel):
    """AddressPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    address_objects = models.ManyToManyField(
        to=AddressObject,
        blank=True,
    )
    address_object_groups = models.ManyToManyField(
        to=AddressObjectGroup,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class UserObject(PrimaryModel, StatusModel):
    """UserObject model."""

    username = models.CharField(
        max_length=50,
        unique=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, blank=True)

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
class UserObjectGroup(PrimaryModel, StatusModel):
    """UserObjectGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(
        to=UserObject,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class UserPolicyObject(PrimaryModel, StatusModel):
    """UserPolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    user_objects = models.ManyToManyField(
        to=UserObject,
        blank=True,
    )
    user_object_groups = models.ManyToManyField(
        to=UserObjectGroup,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class Zone(PrimaryModel, StatusModel):
    """Zone model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    vrfs = models.ManyToManyField(
        to="ipam.VRF",
        blank=True,
    )
    interfaces = models.ManyToManyField(
        to="dcim.Interface",
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class ServiceObject(PrimaryModel, StatusModel):
    """ServiceObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    port = models.IntegerField()
    ip_protocol = models.CharField(choices=choices.IP_PROTOCOL_CHOICES, null=True, blank=True, max_length=20)
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Service Objects"
        constraints = [
            UniqueConstraint(fields=["slug", "port", "ip_protocol"], name="unique_with_ip_protocol"),
            UniqueConstraint(fields=["slug", "port"], condition=Q(ip_protocol=None), name="unique_without_ip_protocol"),
        ]

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
class ServiceObjectGroup(PrimaryModel, StatusModel):
    """ServiceGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class ServicePolicyObject(PrimaryModel, StatusModel):
    """ServicePolicyObject model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    service_objects = models.ManyToManyField(
        to=ServiceObject,
        blank=True,
    )
    service_object_groups = models.ManyToManyField(
        to=ServiceObjectGroup,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
class SourceDestination(PrimaryModel, StatusModel):
    """Source model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    address = models.ForeignKey(to=AddressPolicyObject, on_delete=models.CASCADE)
    service = models.ForeignKey(to=ServicePolicyObject, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserPolicyObject, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

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
            return f"{self.address} - {self.service} - {self.user} - {self.zone}"
        return f"{self.address} - {self.service} - {self.zone}"


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
class PolicyRule(PrimaryModel, StatusModel):
    """PolicyRule model."""

    name = models.CharField(max_length=50, blank=True, null=True)
    tags = TaggableManager(through=TaggedItem)
    index = models.IntegerField()
    source = models.ForeignKey(to=SourceDestination, on_delete=models.CASCADE, related_name="source")
    destination = models.ForeignKey(to=SourceDestination, on_delete=models.CASCADE, related_name="destination")
    action = models.CharField(choices=choices.ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        """Meta class."""

        ordering = ["index"]
        verbose_name_plural = "Policy Rules"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_firewall_models:policyrule", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.name:
            return self.name
        return f"{self.index} - {self.source} - {self.destination} - {self.action}"


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
class Policy(PrimaryModel, StatusModel):
    """Policy model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    role = models.ForeignKey(to=Role, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, unique=True)
    policy_rules = models.ManyToManyField(to=PolicyRule)
    devices = models.ManyToManyField(to="dcim.Device", blank=True)

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
