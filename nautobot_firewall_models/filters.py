"""Filtering for Firewall Model Plugin."""

import django_filters
from django.db.models import Q
from django_filters import CharFilter, FilterSet
from nautobot.dcim.models import Device
from nautobot.extras.filters import StatusModelFilterSetMixin, NautobotFilterSet
from nautobot.utilities.filters import TagFilter

from nautobot_firewall_models import models


class NameDescriptionSearchFilter(FilterSet):
    """A base class for adding the search method to models which only expose the `name` and `description` fields."""

    q = CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):  # pylint: disable=unused-argument, no-self-use
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class IPRangeFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for IPRange."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # fields = ["id", "start_address", "end_address", "vrf", "size", "description"]
        fields = ["id", "vrf", "size", "description"]


class FQDNFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for FQDN."""

    class Meta:
        """Meta attributes for filter."""

        model = models.FQDN

        fields = ["id", "name", "description"]


class AddressObjectFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject

        fields = ["id", "name", "ip_address", "prefix", "ip_range", "fqdn", "description"]


class AddressObjectGroupFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for AddressObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObjectGroup

        fields = ["id", "name", "address_objects", "description"]


class ServiceObjectFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for ServiceObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObject

        fields = ["id", "name", "ip_protocol", "port", "description"]


class ServiceObjectGroupFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for ServiceObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObjectGroup

        fields = ["id", "name", "service_objects", "description"]


class UserObjectFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for UserObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObject
        fields = ["id", "name", "username"]


class UserObjectGroupFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for UserObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObjectGroup
        fields = ["id", "name", "user_objects", "description"]


class ZoneFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for Zone."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Zone

        fields = ["id", "name", "vrfs", "interfaces", "description"]


# TODO: Refactor to allow for better filtering, currently very limited.
class PolicyRuleFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
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
        fields = ["id", "action", "log", "request_id"]


# TODO: Refactor to allow for better filtering, currently very limited.
class NATPolicyRuleFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
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
        fields = ["id", "mode", "log", "request_id"]


class PolicyFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
    """Filter for Policy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Policy
        fields = ["id", "name", "description", "policy_rules", "assigned_devices", "assigned_dynamic_groups"]


class NATPolicyFilterSet(StatusModelFilterSetMixin, NameDescriptionSearchFilter, NautobotFilterSet):
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
