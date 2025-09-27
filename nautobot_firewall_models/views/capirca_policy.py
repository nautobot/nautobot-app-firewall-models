"""Capirca Policy Object Viewsets."""

from nautobot.apps.views import (
    ObjectBulkDestroyViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectListViewMixin,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class CapircaPolicyUIViewSet(
    ObjectListViewMixin,
    ObjectBulkDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
):  # pylint: disable=abstract-method
    """ViewSet for the CapircaPolicy model."""

    bulk_update_form_class = forms.CapircaPolicyBulkEditForm
    filterset_class = filters.CapircaPolicyFilterSet
    filterset_form_class = forms.CapircaPolicyFilterForm
    form_class = forms.CapircaPolicyForm
    queryset = models.CapircaPolicy.objects.all()
    serializer_class = serializers.CapircaPolicySerializer
    table_class = tables.CapircaPolicyTable
    action_buttons = []
    object_detail_content = details.capirca_policy

    lookup_field = "pk"

    @action(detail=True, methods=["get"])
    def devicedetail(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ, unused-argument
        """Action method to see the full configuration."""
        obj = self.get_object()
        device = obj.device
        policy = models.CapircaPolicy.objects.get(device=device)
        context = {"object": policy, "device": device, "active_tab": "devicedetail"}
        return Response(context)
