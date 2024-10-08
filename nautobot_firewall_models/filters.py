"""Filtering for Firewall Model App."""

import django_filters
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db.models import Q
from nautobot.apps.filters import (
    MultiValueCharFilter,
    NaturalKeyOrPKMultipleChoiceFilter,
    NautobotFilterSet,
    StatusModelFilterSetMixin,
)
from nautobot.dcim.models import Device

from nautobot_firewall_models import models


class BaseFilterSet(StatusModelFilterSetMixin, django_filters.filterset.FilterSet):
    """A base class for adding the search method to models which only expose the `name` and `description` fields."""

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):  # pylint: disable=unused-argument
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        return queryset.filter(Q(name__icontains=value) | Q(description__icontains=value))


class IPRangeFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for IPRange."""

    start_address = MultiValueCharFilter(
        method="filter_address",
        label="Address",
    )
    end_address = MultiValueCharFilter(
        method="filter_address",
        label="Address",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]

    def filter_address(self, queryset, name, value):  # pylint: disable=unused-argument
        """Filter method for start & end addresses."""
        try:
            return queryset.net_in(value)
        except ValidationError:
            return queryset.none()


class FQDNFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for FQDN."""

    class Meta:
        """Meta attributes for filter."""

        model = models.FQDN
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class AddressObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class AddressObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for AddressObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObjectGroup
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class ApplicationObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ApplicationObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ApplicationObject
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class ApplicationObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ApplicationObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ApplicationObjectGroup
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class ServiceObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ServiceObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObject
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class ServiceObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for ServiceObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObjectGroup
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class UserObjectFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for UserObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObject
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class UserObjectGroupFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for UserObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObjectGroup
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class ZoneFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for Zone."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Zone
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class PolicyRuleFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for PolicyRule."""

    def search(self, queryset, name, value):  # pylint: disable=unused-argument
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        # pylint: disable=unsupported-binary-operation
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(request_id__icontains=value)
        )

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyRule
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyRuleFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for NATPolicyRule."""

    def search(self, queryset, name, value):  # pylint: disable=unused-argument
        """Construct Q filter for filterset."""
        if not value.strip():
            return queryset
        # pylint: disable=unsupported-binary-operation
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value) | Q(request_id__icontains=value)
        )

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyRule
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class PolicyFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for Policy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Policy
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for NATPolicy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicy
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class CapircaPolicyFilterSet(NautobotFilterSet):
    """Filter for CapircaPolicy."""

    device = NaturalKeyOrPKMultipleChoiceFilter(
        field_name="device",
        queryset=Device.objects.all(),
        to_field_name="name",
        label="Schema (name or PK)",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.CapircaPolicy
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


###########################
# Through Models
###########################


class PolicyDeviceM2MFilterSet(NautobotFilterSet):
    """Filter for PolicyDeviceM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyDeviceM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class PolicyDynamicGroupM2MFilterSet(NautobotFilterSet):
    """Filter for PolicyDynamicGroupM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyDynamicGroupM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyDeviceM2MFilterSet(NautobotFilterSet):
    """Filter for NATPolicyDeviceM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyDeviceM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyDynamicGroupM2MFilterSet(NautobotFilterSet):
    """Filter for NATPolicyDynamicGroupM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyDynamicGroupM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]
