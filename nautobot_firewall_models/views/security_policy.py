"""Rule Object Viewsets."""

from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.views.mixins import PERMISSIONS_ACTION_MAP
from rest_framework.decorators import action

from nautobot_firewall_models.api.serializers import PolicyRuleSerializer, PolicySerializer
from nautobot_firewall_models.filters import PolicyFilterSet, PolicyRuleFilterSet
from nautobot_firewall_models.forms import (
    PolicyBulkEditForm,
    PolicyFilterForm,
    PolicyForm,
    PolicyRuleBulkEditForm,
    PolicyRuleFilterForm,
    PolicyRuleForm,
)
from nautobot_firewall_models.models import (
    Policy,
    PolicyDeviceM2M,
    PolicyDynamicGroupM2M,
    PolicyRule,
    PolicyVirtualMachineM2M,
)
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

    lookup_field = "pk"

    def get_queryset(self):
        """Overload to overwrite permissiosn action map."""
        queryset = super().get_queryset()
        _perms = {
            **PERMISSIONS_ACTION_MAP,
            "devices": "change",
            "virtual_machines": "change",
            "dynamic_groups": "change",
        }
        return queryset.restrict(self.request.user, _perms[self.action])

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
    def virtual_machines(self, request, pk, *args, **kwargs):
        """Method to set weight on a Virtual Machine & Policy Relationship."""
        # pylint: disable=invalid-name, arguments-differ
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for virtual_machine, weight in form_data.items():
            m2m = PolicyVirtualMachineM2M.objects.get(virtual_machine=virtual_machine, policy=pk)
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
