"""Zone Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class ZoneUIViewSet(NautobotUIViewSet):
    """ViewSet for the Zone model."""

    bulk_update_form_class = forms.ZoneBulkEditForm
    filterset_class = filters.ZoneFilterSet
    filterset_form_class = forms.ZoneFilterForm
    form_class = forms.ZoneForm
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    table_class = tables.ZoneTable
    object_detail_content = details.zone

    lookup_field = "pk"
