"""Models for the Firewall plugin."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from django.template.defaultfilters import slugify
from django.urls import reverse
from nautobot.core.models import BaseModel
from nautobot.extras.models.change_logging import ChangeLoggedModel
from nautobot.extras.models.tags import TaggedItem
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from netaddr import IPAddress
from taggit.managers import TaggableManager

from nautobot_plugin_firewall_model.choices import TCP_UDP_CHOICES, ADDRESS_ASSIGNMENT_MODELS, ACTION_CHOICES


@extras_features("custom_validators", "relationships", "graphql")
class IPRange(BaseModel, ChangeLoggedModel):
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
        to="ipam.VRF", on_delete=models.PROTECT, related_name="ip_ranges", blank=True, null=True, verbose_name="VRF"
    )
    description = models.CharField(
        max_length=200,
        blank=True,
    )
    size = models.PositiveIntegerField(editable=False)

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
        return reverse("plugins:nautobot_plugin_firewall_model:iprange", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.start_address}-{self.end_address}"

    def save(self, *args, **kwargs):
        """Overloads to inject size attr."""
        # Record the range's size (number of IP addresses)
        self.size = int(IPAddress(self.end_address) - IPAddress(self.start_address)) + 1

        super().save(*args, **kwargs)


@extras_features("custom_validators", "relationships", "graphql")
class Zone(BaseModel, ChangeLoggedModel):
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

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:zone", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class AddressGroup(BaseModel, ChangeLoggedModel):
    """Zone model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    ip_addresses = models.ManyToManyField(
        to="ipam.IPAddress",
        blank=True,
    )
    ip_ranges = models.ManyToManyField(
        to=IPRange,
        blank=True,
    )
    prefixes = models.ManyToManyField(
        to="ipam.Prefix",
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Zones"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:zone", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class Protocol(BaseModel, ChangeLoggedModel):
    """Zone model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, editable=False)
    port = models.IntegerField()
    tcp_udp = models.CharField(choices=TCP_UDP_CHOICES, null=True, blank=True, max_length=3)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Protocols"
        constraints = [
            UniqueConstraint(fields=["slug", "port", "tcp_udp"], name="unique_with_tcp_udp"),
            UniqueConstraint(fields=["slug", "port"], condition=Q(tcp_udp=None), name="unique_without_tcp_udp"),
        ]

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:protocol", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        if self.tcp_udp:
            return f"{self.slug}:{self.port}:{self.tcp_udp}"
        return f"{self.slug}:{self.port}"

    def save(self, *args, **kwargs):
        """Overloads to enforce use of slugify."""
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)


@extras_features("custom_validators", "relationships", "graphql")
class ServiceGroup(BaseModel, ChangeLoggedModel):
    """ServiceGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    protocols = models.ManyToManyField(
        to=Protocol,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "ServiceGroups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:servicegroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class User(BaseModel, ChangeLoggedModel):
    """ServiceGroup model."""

    username = models.CharField(
        max_length=50,
        unique=True,
    )
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        """Meta class."""

        ordering = ["username"]
        verbose_name_plural = "User"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:user", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.username


@extras_features("custom_validators", "relationships", "graphql")
class UserGroup(BaseModel, ChangeLoggedModel):
    """UserGroup model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(
        to=User,
        blank=True,
    )

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "User Groups"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:usergroup", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name


@extras_features("custom_validators", "relationships", "graphql")
class SourceDestination(BaseModel, ChangeLoggedModel):
    """SourceDestination model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    assigned_address_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=ADDRESS_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )
    assigned_address_id = models.UUIDField(blank=True, null=True)
    address = GenericForeignKey(ct_field="assigned_address_type", fk_field="assigned_address_id")
    address_group = models.ForeignKey(to=AddressGroup, on_delete=models.CASCADE, blank=True, null=True)
    fqdn = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    user_group = models.ForeignKey(to=UserGroup, on_delete=models.CASCADE, blank=True, null=True)
    port = models.IntegerField(blank=True)
    tcp_udp = models.CharField(choices=TCP_UDP_CHOICES, null=True, blank=True, max_length=3)
    service = models.ForeignKey(to=Protocol, on_delete=models.CASCADE)
    service_group = models.ForeignKey(to=ServiceGroup, on_delete=models.CASCADE)
    zone = models.ForeignKey(to=Zone, on_delete=models.CASCADE)

    class Meta:
        """Meta class."""

        ordering = ["description"]
        verbose_name_plural = "Sources or Destinations"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:sourcedestination", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        # TODO: Need to determine better __str__
        return self.description


@extras_features("custom_validators", "relationships", "graphql")
class Term(BaseModel, ChangeLoggedModel):
    """Term model."""

    tags = TaggableManager(through=TaggedItem)
    index = models.IntegerField()
    source = models.ForeignKey(to=SourceDestination, on_delete=models.CASCADE, related_name="%(class)s_source")
    destination = models.ForeignKey(
        to=SourceDestination, on_delete=models.CASCADE, related_name="%(class)s_destination"
    )
    action = models.CharField(choices=ACTION_CHOICES, max_length=20)
    log = models.BooleanField(default=False)

    class Meta:
        """Meta class."""

        ordering = ["index"]
        verbose_name_plural = "Terms"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:term", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return f"{self.index} - {self.source} - {self.destination} - {self.action}"


@extras_features("custom_validators", "relationships", "graphql")
class Policy(BaseModel, ChangeLoggedModel):
    """Policy model."""

    description = models.CharField(
        max_length=200,
        blank=True,
    )
    name = models.CharField(max_length=50, unique=True)
    terms = models.ManyToManyField(to=Term)

    class Meta:
        """Meta class."""

        ordering = ["name"]
        verbose_name_plural = "Policies"

    def get_absolute_url(self):
        """Return detail view URL."""
        return reverse("plugins:nautobot_plugin_firewall_model:policy", args=[self.pk])

    def __str__(self):
        """Stringify instance."""
        return self.name
