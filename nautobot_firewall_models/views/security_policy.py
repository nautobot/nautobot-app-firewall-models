"""Rule Object Viewsets."""

from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.views import NautobotUIViewSet
from rest_framework.decorators import action

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class PolicyRuleUIViewSet(NautobotUIViewSet):
    """ViewSet for the PolicyRule model."""

    bulk_update_form_class = forms.PolicyRuleBulkEditForm
    filterset_class = filters.PolicyRuleFilterSet
    filterset_form_class = forms.PolicyRuleFilterForm
    form_class = forms.PolicyRuleForm
    queryset = models.PolicyRule.objects.all()
    serializer_class = serializers.PolicyRuleSerializer
    table_class = tables.PolicyRuleTable
    object_detail_content = details.policy_rule

    lookup_field = "pk"


class PolicyUIViewSet(NautobotUIViewSet):
    """ViewSet for the Policy model."""

    bulk_update_form_class = forms.PolicyBulkEditForm
    filterset_class = filters.PolicyFilterSet
    filterset_form_class = forms.PolicyFilterForm
    form_class = forms.PolicyForm
    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    table_class = tables.PolicyTable
    object_detail_content = details.policy
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

    def get_extra_context(self, request, instance=None):
        """Add extra permissions for edit-device-weight and edit-dynamicgroup-weight tabs."""
        context = super().get_extra_context(request, instance)
        context["device_weight_tab_perms"] = ["dcim.change_device", "nautobot_firewall_models.change_policy"]
        context["dynamicgroup_weight_tab_perms"] = [
            "extras.change_dynamicgroup",
            "nautobot_firewall_models.change_policy",
        ]

        return context

    @action(
        detail=True,
        methods=["post"],
        custom_view_base_action="change",
        custom_view_additional_permissions=["dcim.change_device"],
    )
    def devices(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = models.PolicyDeviceM2M.objects.get(device=device, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))

    @action(
        detail=True,
        methods=["post"],
        custom_view_base_action="change",
        custom_view_additional_permissions=["extras.change_dynamicgroup"],
    )
    def dynamic_groups(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = models.PolicyDynamicGroupM2M.objects.get(dynamic_group=group, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))
