"""NAT Rule Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models.api.serializers import NATPolicyRuleSerializer, NATPolicySerializer
from nautobot_firewall_models.filters import NATPolicyRuleFilterSet, NATPolicyFilterSet
from nautobot_firewall_models.forms import (
    NATPolicyRuleBulkEditForm,
    NATPolicyRuleFilterForm,
    NATPolicyRuleForm,
    NATPolicyBulkEditForm,
    NATPolicyFilterForm,
    NATPolicyForm,
)
from nautobot_firewall_models.models import NATPolicyRule, NATPolicy
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
    action_buttons = ("add",)

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
    action_buttons = ("add",)

    lookup_field = "pk"
