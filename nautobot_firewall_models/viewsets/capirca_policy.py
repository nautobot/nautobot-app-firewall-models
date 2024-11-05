"""Capirca Policy Object Viewsets."""

from nautobot.apps.views import (
    ObjectBulkDestroyViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectListViewMixin,
)
from nautobot.dcim.models import Device
from rest_framework.response import Response

from nautobot_firewall_models import filters, forms, models, tables
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
    action_buttons = None

    lookup_field = "pk"


class CapircaPolicyDeviceUIViewSet(ObjectDetailViewMixin):  # pylint: disable=abstract-method
    """ViewSet for the CapircaPolicy Device Details."""

    queryset = Device.objects.all()
    lookup_field = "pk"

    def get_template_name(self):
        """Set template name."""
        return "nautobot_firewall_models/capircapolicy_details.html"

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a model instance."""
        device = self.get_object()
        policy = models.CapircaPolicy.objects.get(device=device)
        context = {"object": policy, "device": device}
        context["use_new_ui"] = True
        return Response(context)
