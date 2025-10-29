"""Models for the Firewall app."""
# pylint: disable=duplicate-code

from django.db import models
from nautobot.apps.constants import CHARFIELD_MAX_LENGTH
from nautobot.core.models.generics import PrimaryModel
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
        max_length=CHARFIELD_MAX_LENGTH,
        unique=True,
        help_text="Signifies the username in identify provider (e.g. john.smith)",
    )
    name = models.CharField(
        max_length=CHARFIELD_MAX_LENGTH,
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
        max_length=1024,
        blank=True,
    )
    name = models.CharField(max_length=CHARFIELD_MAX_LENGTH, unique=True)
    user_objects = models.ManyToManyField(
        to="nautobot_firewall_models.UserObject",
        blank=True,
        related_name="user_object_groups",
        verbose_name="User Objects",
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

    def __str__(self):
        """Stringify instance."""
        return self.name
