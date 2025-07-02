"""Aerleon Policy Object Viewsets."""

from nautobot.apps.views import (
    ObjectBulkDestroyViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectListViewMixin,
)

from nautobot_firewall_models import filters, forms, models, tables
from nautobot_firewall_models.api import serializers
from nautobot_firewall_models.models import AerleonPolicy


class AerleonPolicyUIViewSet(
    ObjectListViewMixin,
    ObjectBulkDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
):  # pylint: disable=abstract-method
    """ViewSet for the AerleonPolicy model."""

    bulk_update_form_class = forms.AerleonPolicyBulkEditForm
    filterset_class = filters.AerleonPolicyFilterSet
    filterset_form_class = forms.AerleonPolicyFilterForm
    queryset = models.AerleonPolicy.objects.all()
    serializer_class = serializers.AerleonPolicySerializer
    table_class = tables.AerleonPolicyTable
    action_buttons = []

    lookup_field = "pk"


class AerleonPolicyDeviceUIViewSet(ObjectDetailViewMixin):  # pylint: disable=abstract-method
    """ViewSet for the AerleonPolicy Device Details."""

    queryset = AerleonPolicy.objects.all()
    lookup_field = "pk"

    def get_template_name(self):
        """Set template name."""
        return "nautobot_firewall_models/aerleonpolicy_details.html"
