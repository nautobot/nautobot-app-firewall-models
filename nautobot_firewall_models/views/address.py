"""Address Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class AddressObjectUIViewSet(NautobotUIViewSet):
    """ViewSet for the AddressObject model."""

    bulk_update_form_class = forms.AddressObjectBulkEditForm
    filterset_class = filters.AddressObjectFilterSet
    filterset_form_class = forms.AddressObjectFilterForm
    form_class = forms.AddressObjectForm
    queryset = models.AddressObject.objects.all()
    serializer_class = serializers.AddressObjectSerializer
    table_class = tables.AddressObjectTable
    object_detail_content = details.address_object

    lookup_field = "pk"


class AddressObjectGroupUIViewSet(NautobotUIViewSet):
    """ViewSet for the AddressObjectGroup model."""

    bulk_update_form_class = forms.AddressObjectGroupBulkEditForm
    filterset_class = filters.AddressObjectGroupFilterSet
    filterset_form_class = forms.AddressObjectGroupFilterForm
    form_class = forms.AddressObjectGroupForm
    queryset = models.AddressObjectGroup.objects.all()
    serializer_class = serializers.AddressObjectGroupSerializer
    table_class = tables.AddressObjectGroupTable
    object_detail_content = details.address_object_group

    lookup_field = "pk"


class FQDNUIViewSet(NautobotUIViewSet):
    """ViewSet for the FQDN model."""

    bulk_update_form_class = forms.FQDNBulkEditForm
    filterset_class = filters.FQDNFilterSet
    filterset_form_class = forms.FQDNFilterForm
    form_class = forms.FQDNForm
    queryset = models.FQDN.objects.all()
    serializer_class = serializers.FQDNSerializer
    table_class = tables.FQDNTable
    object_detail_content = details.fqdn

    lookup_field = "pk"


class IPRangeUIViewSet(NautobotUIViewSet):
    """ViewSet for the IPRange model."""

    bulk_update_form_class = forms.IPRangeBulkEditForm
    filterset_class = filters.IPRangeFilterSet
    filterset_form_class = forms.IPRangeFilterForm
    form_class = forms.IPRangeForm
    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    table_class = tables.IPRangeTable
    object_detail_content = details.ip_range

    lookup_field = "pk"
