"""Capirca Policy Object Viewsets."""

from nautobot.apps.views import (
    ObjectListViewMixin,
    ObjectBulkDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
)

from nautobot_firewall_models.api import serializers
from nautobot_firewall_models import forms, models, tables, filters


class CapircaPolicyUIViewSet(
    ObjectListViewMixin,
    ObjectBulkDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
):
    """ViewSet for the CapircaPolicy model."""

    bulk_update_form_class = forms.CapircaPolicyBulkEditForm
    filterset_class = filters.CapircaPolicyFilterSet
    filterset_form_class = forms.CapircaPolicyFilterForm
    form_class = forms.CapircaPolicyForm
    queryset = models.CapircaPolicy.objects.all()
    serializer_class = serializers.CapircaPolicySerializer
    table_class = tables.CapircaPolicyTable
    action_buttons = ("add",)

    lookup_field = "pk"

    def _process_bulk_create_form(self, *args, **kwargs):
        """Not implemented."""

    def _process_bulk_update_form(self, *args, **kwargs):
        """Not implemented."""

    def _process_create_or_update_form(self, *args, **kwargs):
        """Not implemented."""
