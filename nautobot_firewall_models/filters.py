"""Filtering for Firewall Model Plugin."""

import django_filters
from django.db.models import Q
from django_filters import CharFilter
from django_filters.filterset import FilterSet
from nautobot.dcim.models import Device
from nautobot.extras.filters import NautobotFilterSet
from nautobot.extras.models import Status
from nautobot.utilities.filters import TagFilter

from nautobot_firewall_models import models


class BaseFilterSet(FilterSet):
    """A base class for adding the search method to models which only expose the `name` and `description` fields."""

    q = CharFilter(
        method="search",
        label="Search",
    )
    status = django_filters.ModelMultipleChoiceFilter(
        field_name="status__slug",
        to_field_name="slug",
        queryset=Status.objects.all(),
    )

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class IPRangeFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for IPRange."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # fields = ["id", "start_address", "end_address", "vrf", "size", "description"]
        fields = ["id", "vrf", "size", "description"]


class FQDNFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for FQDN."""

    class Meta:
        """Meta attributes for filter."""

        model = models.FQDN

        fields = ["id", "name", "description"]


class AddressObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject

        fields = ["id", "name", "ip_address", "prefix", "ip_range", "fqdn", "description"]


class AddressObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for AddressObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObjectGroup

        fields = ["id", "name", "address_objects", "description"]


class ApplicationObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ApplicationObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ApplicationObject

        fields = ["id", "name", "description", "category", "subcategory", "risk"]


class ApplicationObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ApplicationObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ApplicationObjectGroup

        fields = ["id", "name", "application_objects", "description"]


class ServiceObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ServiceObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObject

        fields = ["id", "name", "ip_protocol", "port", "description"]


class ServiceObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ServiceObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObjectGroup

        fields = ["id", "name", "service_objects", "description"]


class UserObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for UserObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObject
        fields = ["id", "name", "username"]


class UserObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for UserObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObjectGroup
        fields = ["id", "name", "user_objects", "description"]


class ZoneFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for Zone."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Zone

        fields = ["id", "name", "vrfs", "interfaces", "description"]


# TODO: Refactor to allow for better filtering, currently very limited.
class PolicyRuleFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for PolicyRule."""

    tag = TagFilter()

    q = CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(request_id__icontains=value)
        )

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyRule
        fields = ["id", "action", "log", "request_id", "description"]


# TODO: Refactor to allow for better filtering, currently very limited.
class NATPolicyRuleFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for NATPolicyRule."""

    tag = TagFilter()

    q = CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(request_id__icontains=value)
        )

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyRule
        fields = ["id", "remark", "log", "request_id"]


class PolicyFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for Policy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Policy
        fields = ["id", "name", "description", "policy_rules", "assigned_devices", "assigned_dynamic_groups"]

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        """Overload init to allow for deep=True on detail API call."""
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.data.pop("deep", None)


class NATPolicyFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for NATPolicy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicy
        fields = ["id", "name", "description", "nat_policy_rules", "assigned_devices", "assigned_dynamic_groups"]


class CapircaPolicyFilterSet(NautobotFilterSet):
    """Filter for CapircaPolicy."""

    device = django_filters.ModelMultipleChoiceFilter(
        field_name="device__name",
        queryset=Device.objects.all(),
        to_field_name="name",
        label="Device Name",
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label="Device ID",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.CapircaPolicy
        fields = ["id"]
