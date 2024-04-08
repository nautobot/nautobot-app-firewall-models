"""Aerleon Policy Object Viewsets."""

from nautobot.apps.views import (
    ObjectListViewMixin,
    ObjectBulkDestroyViewMixin,
    ObjectDetailViewMixin,
    ObjectChangeLogViewMixin,
    ObjectDestroyViewMixin,
)
from nautobot.dcim.models import Device
from rest_framework.response import Response

from nautobot_firewall_models.api import serializers
from nautobot_firewall_models import forms, models, tables, filters


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
    form_class = forms.AerleonPolicyForm
    queryset = models.AerleonPolicy.objects.all()
    serializer_class = serializers.AerleonPolicySerializer
    table_class = tables.AerleonPolicyTable
    action_buttons = None

    lookup_field = "pk"


class AerleonPolicyDeviceUIViewSet(ObjectDetailViewMixin):  # pylint: disable=abstract-method
    """ViewSet for the AerleonPolicy Device Details."""

    queryset = Device.objects.all()
    lookup_field = "pk"

    def get_template_name(self):
        """Set template name."""
        return "nautobot_firewall_models/aerleonpolicy_details.html"

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a model instance."""
        device = self.get_object()
        policy = models.AerleonPolicy.objects.get(device=device)
        context = {"object": policy, "device": device}
        context["use_new_ui"] = True
        return Response(context)
