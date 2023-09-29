"""Zone Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models.api import serializers
from nautobot_firewall_models import forms, models, tables, filters


class ZoneUIViewSet(NautobotUIViewSet):
    """ViewSet for the Zone model."""

    bulk_update_form_class = forms.ZoneBulkEditForm
    filterset_class = filters.ZoneFilterSet
    filterset_form_class = forms.ZoneFilterForm
    form_class = forms.ZoneForm
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    table_class = tables.ZoneTable
    action_buttons = ("add",)

    lookup_field = "pk"
