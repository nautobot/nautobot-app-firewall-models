"""NAT Rule Object Viewsets."""

from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.views.mixins import PERMISSIONS_ACTION_MAP
from rest_framework.decorators import action

from nautobot_firewall_models.api.serializers import NATPolicyRuleSerializer, NATPolicySerializer
from nautobot_firewall_models.filters import NATPolicyFilterSet, NATPolicyRuleFilterSet
from nautobot_firewall_models.forms import (
    NATPolicyBulkEditForm,
    NATPolicyFilterForm,
    NATPolicyForm,
    NATPolicyRuleBulkEditForm,
    NATPolicyRuleFilterForm,
    NATPolicyRuleForm,
)
from nautobot_firewall_models.models import NATPolicy, NATPolicyDeviceM2M, NATPolicyDynamicGroupM2M, NATPolicyRule
from nautobot_firewall_models.tables import NATPolicyRuleTable, NATPolicyTable


class NATPolicyRuleUIViewSet(NautobotUIViewSet):
    """ViewSet for the NATPolicyRule model."""

    bulk_update_form_class = NATPolicyRuleBulkEditForm
    filterset_class = NATPolicyRuleFilterSet
    filterset_form_class = NATPolicyRuleFilterForm
    form_class = NATPolicyRuleForm
    queryset = NATPolicyRule.objects.all()
    serializer_class = NATPolicyRuleSerializer
    table_class = NATPolicyRuleTable

    lookup_field = "pk"


class NATPolicyUIViewSet(NautobotUIViewSet):
    """ViewSet for the NATPolicy model."""

    bulk_update_form_class = NATPolicyBulkEditForm
    filterset_class = NATPolicyFilterSet
    filterset_form_class = NATPolicyFilterForm
    form_class = NATPolicyForm
    queryset = NATPolicy.objects.all()
    serializer_class = NATPolicySerializer
    table_class = NATPolicyTable
    prefetch_related = [
        "nat_policy_rules__source_users",
        "nat_policy_rules__source_user_groups",
        "nat_policy_rules__source_zone",
        "nat_policy_rules__destination_zone",
        "nat_policy_rules__original_source_addresses",
        "nat_policy_rules__original_source_address_groups",
        "nat_policy_rules__original_source_services",
        "nat_policy_rules__original_source_service_groups",
        "nat_policy_rules__translated_source_addresses",
        "nat_policy_rules__translated_source_address_groups",
        "nat_policy_rules__translated_source_services",
        "nat_policy_rules__translated_source_service_groups",
        "nat_policy_rules__original_destination_addresses",
        "nat_policy_rules__original_destination_address_groups",
        "nat_policy_rules__original_destination_services",
        "nat_policy_rules__original_destination_service_groups",
        "nat_policy_rules__translated_destination_addresses",
        "nat_policy_rules__translated_destination_address_groups",
        "nat_policy_rules__translated_destination_services",
        "nat_policy_rules__translated_destination_service_groups",
    ]

    lookup_field = "pk"

    @action(detail=True, methods=["post"])
    def devices(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & NATPolicy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = NATPolicyDeviceM2M.objects.get(device=device, nat_policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:natpolicy", kwargs={"pk": pk}))

    @action(detail=True, methods=["post"])
    def dynamic_groups(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = NATPolicyDynamicGroupM2M.objects.get(dynamic_group=group, nat_policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:natpolicy", kwargs={"pk": pk}))

    def get_queryset(self):
        """Overload to overwrite permissiosn action map."""
        queryset = super().get_queryset()
        _perms = {**PERMISSIONS_ACTION_MAP, "devices": "change", "dynamic_groups": "change"}
        return queryset.restrict(self.request.user, _perms[self.action])
