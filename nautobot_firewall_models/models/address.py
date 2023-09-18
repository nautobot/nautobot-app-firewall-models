"""Models for the Firewall plugin."""
# pylint: disable=duplicate-code, too-many-lines

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint
from nautobot.core.models.generics import BaseModel, PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features
from nautobot.ipam.fields import VarbinaryIPField
from netaddr import IPAddress

from nautobot_firewall_models.utils import get_default_status


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
        verbose_name = "IP Range"
        verbose_name_plural = "IP Ranges"
        constraints = [
            UniqueConstraint(fields=["start_address", "end_address", "vrf"], name="unique_with_vrf"),
            UniqueConstraint(fields=["start_address", "end_address"], condition=Q(vrf=None), name="unique_without_vrf"),
        ]

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
        max_length=254, unique=True, help_text="Resolvable fully qualified domain name (e.g. networktocode.com)"
    )
    ip_addresses = models.ManyToManyField(
        to="ipam.IPAddress",
        related_name="fqdns",
        blank=True,
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
    fqdn = models.ForeignKey(to="nautobot_firewall_models.FQDN", on_delete=models.PROTECT, null=True, blank=True)
    ip_range = models.ForeignKey(to="nautobot_firewall_models.IPRange", on_delete=models.PROTECT, null=True, blank=True)
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

    def get_address_info(self):
        """Method to Return the actual AddressObject type."""
        keys = ["ip_range", "fqdn", "prefix", "ip_address"]
        for key in keys:
            if getattr(self, key):
                return (key, getattr(self, key))
        return (None, None)

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
        to="nautobot_firewall_models.AddressObject",
        related_name="address_object_groups",
        blank=True,
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

    def __str__(self):
        """Stringify instance."""
        return self.name
