"""Rule Object Viewsets."""
from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.views.mixins import PERMISSIONS_ACTION_MAP
from rest_framework.decorators import action

from nautobot_firewall_models.api.serializers import PolicyRuleSerializer, PolicySerializer
from nautobot_firewall_models.filters import PolicyRuleFilterSet, PolicyFilterSet
from nautobot_firewall_models.forms import (
    PolicyRuleBulkEditForm,
    PolicyRuleFilterForm,
    PolicyRuleForm,
    PolicyBulkEditForm,
    PolicyFilterForm,
    PolicyForm,
)
from nautobot_firewall_models.models import PolicyRule, Policy, PolicyDeviceM2M, PolicyDynamicGroupM2M
from nautobot_firewall_models.tables import PolicyRuleTable, PolicyTable


class PolicyRuleUIViewSet(NautobotUIViewSet):
    """ViewSet for the PolicyRule model."""

    bulk_update_form_class = PolicyRuleBulkEditForm
    filterset_class = PolicyRuleFilterSet
    filterset_form_class = PolicyRuleFilterForm
    form_class = PolicyRuleForm
    queryset = PolicyRule.objects.all()
    serializer_class = PolicyRuleSerializer
    table_class = PolicyRuleTable
    action_buttons = ("add",)

    lookup_field = "pk"


class PolicyUIViewSet(NautobotUIViewSet):
    """ViewSet for the Policy model."""

    bulk_update_form_class = PolicyBulkEditForm
    filterset_class = PolicyFilterSet
    filterset_form_class = PolicyFilterForm
    form_class = PolicyForm
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    table_class = PolicyTable
    prefetch_related = [
        "policy_rules__source_users",
        "policy_rules__source_user_groups",
        "policy_rules__source_zone",
        "policy_rules__destination_zone",
        "policy_rules__original_source_addresses",
        "policy_rules__original_source_address_groups",
        "policy_rules__original_source_services",
        "policy_rules__original_source_service_groups",
        "policy_rules__translated_source_addresses",
        "policy_rules__translated_source_address_groups",
        "policy_rules__translated_source_services",
        "policy_rules__translated_source_service_groups",
        "policy_rules__original_destination_addresses",
        "policy_rules__original_destination_address_groups",
        "policy_rules__original_destination_services",
        "policy_rules__original_destination_service_groups",
        "policy_rules__translated_destination_addresses",
        "policy_rules__translated_destination_address_groups",
        "policy_rules__translated_destination_services",
        "policy_rules__translated_destination_service_groups",
    ]
    action_buttons = ("add",)

    lookup_field = "pk"

    def get_queryset(self):
        """Overload to overwrite permissiosn action map."""
        PERMISSIONS_ACTION_MAP.update({"devices": "devices", "dynamic_groups": "dynamic_groups"})
        return super().get_queryset()

    @action(detail=True, methods=["post"])
    def devices(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = PolicyDeviceM2M.objects.get(device=device, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))

    @action(detail=True, methods=["post"])
    def dynamic_groups(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = PolicyDynamicGroupM2M.objects.get(dynamic_group=group, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))
