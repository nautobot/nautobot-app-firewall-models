"""Filtering for nautobot_firewall_models."""

import django_filters
from django.contrib.contenttypes.fields import GenericRelation
from nautobot.apps.filters import (
    MultiValueCharFilter,
    NaturalKeyOrPKMultipleChoiceFilter,
    NautobotFilterSet,
    SearchFilter,
    StatusModelFilterSetMixin,
)
from nautobot.dcim.models import Device

from nautobot_firewall_models import models


class IPRangeFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for IPRange."""

    start_address = MultiValueCharFilter(
        label="Address",
    )
    end_address = MultiValueCharFilter(
        label="Address",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
