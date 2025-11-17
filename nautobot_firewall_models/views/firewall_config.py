"""Firewall Config Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class FirewallConfigUIViewSet(NautobotUIViewSet):
    """ViewSet for the FirewallConfig model."""

    bulk_update_form_class = forms.FirewallConfigBulkEditForm
    filterset_class = filters.FirewallConfigFilterSet
    filterset_form_class = forms.FirewallConfigFilterForm
    form_class = forms.FirewallConfigForm
    queryset = models.FirewallConfig.objects.all()
    serializer_class = serializers.FirewallConfigSerializer
    table_class = tables.FirewallConfigTable
    object_detail_content = details.firewall_config

    lookup_field = "pk"

    @action(detail=True, methods=["get"])
    def devicedetail(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ, unused-argument
        """Action method to see the full configuration."""
        obj = self.get_object()
        device = obj.device
        context = {"object": obj, "device": device, "active_tab": "devicedetail"}
        return Response(context)
