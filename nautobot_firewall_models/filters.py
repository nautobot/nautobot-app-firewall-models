"""Filtering for nautobot_firewall_models."""

from nautobot.apps.filters import NameSearchFilterSet, NautobotFilterSet

from nautobot_firewall_models import models


class IPRangeFilterSet(NameSearchFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
    """Filter for IPRange."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # add any fields from the model that you would like to filter your searches by using those
        fields = "__all__"
