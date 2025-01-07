"""Views for nautobot_firewall_models."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class IPRangeUIViewSet(NautobotUIViewSet):
    """ViewSet for IPRange views."""

    bulk_update_form_class = forms.IPRangeBulkEditForm
    filterset_class = filters.IPRangeFilterSet
    filterset_form_class = forms.IPRangeFilterForm
    form_class = forms.IPRangeForm
    lookup_field = "pk"
    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    table_class = tables.IPRangeTable
