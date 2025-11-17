"""NAT Rule Object Viewsets."""

from django.shortcuts import redirect
from django.urls import reverse
from nautobot.apps.views import NautobotUIViewSet
from nautobot.core.views.mixins import PERMISSIONS_ACTION_MAP
from rest_framework.decorators import action

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class NATPolicyRuleUIViewSet(NautobotUIViewSet):
    """ViewSet for the NATPolicyRule model."""

    bulk_update_form_class = forms.NATPolicyRuleBulkEditForm
    filterset_class = filters.NATPolicyRuleFilterSet
    filterset_form_class = forms.NATPolicyRuleFilterForm
    form_class = forms.NATPolicyRuleForm
    queryset = models.NATPolicyRule.objects.all()
    serializer_class = serializers.NATPolicyRuleSerializer
    table_class = tables.NATPolicyRuleTable
    object_detail_content = details.nat_policy_rule

    lookup_field = "pk"


class NATPolicyUIViewSet(NautobotUIViewSet):
    """ViewSet for the NATPolicy model."""

    bulk_update_form_class = forms.NATPolicyBulkEditForm
    filterset_class = filters.NATPolicyFilterSet
    filterset_form_class = forms.NATPolicyFilterForm
    form_class = forms.NATPolicyForm
    queryset = models.NATPolicy.objects.all()
    serializer_class = serializers.NATPolicySerializer
    table_class = tables.NATPolicyTable
    object_detail_content = details.nat_policy
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

    def get_extra_context(self, request, instance=None):
        """Add extra permissions for edit-device-weight and edit-dynamicgroup-weight tabs."""
        context = super().get_extra_context(request, instance)
        context["device_weight_tab_perms"] = ["dcim.change_device", "nautobot_firewall_models.change_natpolicy"]
        context["dynamicgroup_weight_tab_perms"] = [
            "extras.change_dynamicgroup",
            "nautobot_firewall_models.change_natpolicy",
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
        """Method to set weight on a Device & NATPolicy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = models.NATPolicyDeviceM2M.objects.get(device=device, nat_policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:natpolicy", kwargs={"pk": pk}))

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
            m2m = models.NATPolicyDynamicGroupM2M.objects.get(dynamic_group=group, nat_policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:natpolicy", kwargs={"pk": pk}))
