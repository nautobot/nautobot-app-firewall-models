"""NATPolicy Object Views."""

from django.shortcuts import reverse, redirect
from django.views.generic.edit import CreateView
from nautobot.core.views import mixins

from nautobot_firewall_models import models
from nautobot_firewall_models.api.serializers import NATPolicySerializer
from nautobot_firewall_models.filters import NATPolicyFilterSet
from nautobot_firewall_models.forms import NATPolicyBulkEditForm, NATPolicyFilterForm, NATPolicyForm
from nautobot_firewall_models.models import NATPolicy
from nautobot_firewall_models.tables import NATPolicyTable


class NATPolicyUIViewSet(
    mixins.ObjectDetailViewMixin,
    mixins.ObjectListViewMixin,
    mixins.ObjectEditViewMixin,
    mixins.ObjectDestroyViewMixin,
    mixins.ObjectBulkDestroyViewMixin,
    mixins.ObjectBulkUpdateViewMixin,
):
    """ViewSet for the NATPolicy model."""

    bulk_update_form_class = NATPolicyBulkEditForm
    filterset_class = NATPolicyFilterSet
    filterset_form_class = NATPolicyFilterForm
    form_class = NATPolicyForm
    queryset = NATPolicy.objects.all()
    serializer_class = NATPolicySerializer
    table_class = NATPolicyTable
    prefetch_related = [
        "natpolicyrulem2m_set__nat_rule__source_users",
        "natpolicyrulem2m_set__nat_rule__source_user_groups",
        "natpolicyrulem2m_set__nat_rule__source_zone",
        "natpolicyrulem2m_set__nat_rule__destination_zone",
        "natpolicyrulem2m_set__nat_rule__original_source_addresses",
        "natpolicyrulem2m_set__nat_rule__original_source_address_groups",
        "natpolicyrulem2m_set__nat_rule__original_source_services",
        "natpolicyrulem2m_set__nat_rule__original_source_service_groups",
        "natpolicyrulem2m_set__nat_rule__translated_source_addresses",
        "natpolicyrulem2m_set__nat_rule__translated_source_address_groups",
        "natpolicyrulem2m_set__nat_rule__translated_source_services",
        "natpolicyrulem2m_set__nat_rule__translated_source_service_groups",
        "natpolicyrulem2m_set__nat_rule__original_destination_addresses",
        "natpolicyrulem2m_set__nat_rule__original_destination_address_groups",
        "natpolicyrulem2m_set__nat_rule__original_destination_services",
        "natpolicyrulem2m_set__nat_rule__original_destination_service_groups",
        "natpolicyrulem2m_set__nat_rule__translated_destination_addresses",
        "natpolicyrulem2m_set__nat_rule__translated_destination_address_groups",
        "natpolicyrulem2m_set__nat_rule__translated_destination_services",
        "natpolicyrulem2m_set__nat_rule__translated_destination_service_groups",
    ]
    action_buttons = ("add",)

    lookup_field = "pk"


class NATPolicyDynamicGroupWeight(CreateView):
    """View to set weight on a DynamicGroup/NATPolicy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = models.NATPolicyDynamicGroupM2M.objects.get(dynamic_group=group, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:nat_policy", kwargs={"pk": pk}))


class NATPolicyDeviceWeight(CreateView):
    """View to set weight on a Device/NATPolicy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & NATPolicy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = models.NATPolicyDeviceM2M.objects.get(device=device, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:nat_policy", kwargs={"pk": pk}))
