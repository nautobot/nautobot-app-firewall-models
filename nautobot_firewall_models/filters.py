"""Filtering for nautobot_firewall_models."""

import django_filters
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django_filters import ModelMultipleChoiceFilter
from nautobot.apps.filters import (
    MultiValueCharFilter,
    NautobotFilterSet,
    SearchFilter,
    StatusModelFilterSetMixin,
)
from nautobot.dcim.models import Device
from nautobot.virtualization.models import VirtualMachine

from nautobot_firewall_models import models


class BaseFilterSet(StatusModelFilterSetMixin, django_filters.filterset.FilterSet):
    """A base class for adding the search method to models which only expose the `name` and `description` fields."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
        }
    )


class IPRangeFilterSet(BaseFilterSet, NautobotFilterSet):  # pylint: disable=too-many-ancestors
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

        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


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

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "request_id": "icontains",
        }
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyRule
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyRuleFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for NATPolicyRule."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "description": "icontains",
            "request_id": "icontains",
        }
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


class AerleonPolicyFilterSet(BaseFilterSet, NautobotFilterSet):
    """Filter for AerleonPolicy."""

    device_id = ModelMultipleChoiceFilter(
        field_name="device",
        queryset=Device.objects.all(),
        to_field_name="pk",
        label="Device (name or PK)",
        method="filter_device",
    )

    device = ModelMultipleChoiceFilter(
        field_name="device",
        queryset=Device.objects.all(),
        to_field_name="name",
        label="Device (name or PK)",
        method="filter_device",
    )

    virtual_machine_id = ModelMultipleChoiceFilter(
        field_name="virtual_machine",
        queryset=VirtualMachine.objects.all(),
        to_field_name="pk",
        label="Virtual Machine (name or PK)",
        method="filter_virtual_machine",
    )

    virtual_machine = ModelMultipleChoiceFilter(
        field_name="virtual_machine",
        queryset=VirtualMachine.objects.all(),
        to_field_name="name",
        label="Virtual Machine (name or PK)",
        method="filter_virtual_machine",
    )

    class Meta:
        """Meta attributes for filter."""

        model = models.AerleonPolicy
        fields = [
            i.name
            for i in model._meta.get_fields()
            if not isinstance(i, GenericRelation) and not isinstance(i, GenericForeignKey)
        ] + ["device", "virtual_machine"]

    @staticmethod
    def filter_device(queryset, _, value):
        """Dedicated filter method for device form field (needed because of the use of ContentType)."""
        if not value:
            return queryset

        ct = ContentType.objects.get_for_model(Device)

        return queryset.filter(content_type=ct, object_id__in=[v.id for v in value])

    @staticmethod
    def filter_virtual_machine(queryset, _, value):
        """Dedicated filter method for virtual_machine form field (needed because of the use of ContentType)."""
        if not value:
            return queryset

        ct = ContentType.objects.get_for_model(VirtualMachine)

        return queryset.filter(content_type=ct, object_id__in=[v.id for v in value])


###########################
# Through Models
###########################


class PolicyDeviceM2MFilterSet(NautobotFilterSet):
    """Filter for PolicyDeviceM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyDeviceM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class PolicyVirtualMachineM2MFilterSet(NautobotFilterSet):
    """Filter for PolicyVirtualMachineM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyVirtualMachineM2M
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


class NATPolicyVirtualMachineM2MFilterSet(NautobotFilterSet):
    """Filter for NATPolicyVirtualMachineM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyVirtualMachineM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]


class NATPolicyDynamicGroupM2MFilterSet(NautobotFilterSet):
    """Filter for NATPolicyDynamicGroupM2M."""

    class Meta:
        """Meta attributes for filter."""

        model = models.NATPolicyDynamicGroupM2M
        fields = [i.name for i in model._meta.get_fields() if not isinstance(i, GenericRelation)]
