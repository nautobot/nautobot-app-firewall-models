"""Models for the Firewall plugin."""
# pylint: disable=duplicate-code

from django.db import models
from django.urls import reverse
from nautobot.core.models.generics import BaseModel, PrimaryModel
from nautobot.extras.models import StatusField
from nautobot.extras.utils import extras_features

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
class UserObject(PrimaryModel):
    """Source users can be used to identify the origin of traffic for a user on some firewalls."""

    username = models.CharField(
        max_length=100, unique=True, help_text="Signifies the username in identify provider (e.g. john.smith)"
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Signifies the name of the user, commonly first & last name (e.g. John Smith)",
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
        to="nautobot_firewall_models.UserObject",
        blank=True,
        through="UserObjectGroupM2M",
        related_name="user_object_groups",
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


###########################
# Through Models
###########################


class UserObjectGroupM2M(BaseModel):
    """Custom through model to on_delete=models.PROTECT to prevent deleting associated User if assigned to a UserGroup."""

    user = models.ForeignKey("nautobot_firewall_models.UserObject", on_delete=models.PROTECT)
    user_group = models.ForeignKey("nautobot_firewall_models.UserObjectGroup", on_delete=models.CASCADE)
