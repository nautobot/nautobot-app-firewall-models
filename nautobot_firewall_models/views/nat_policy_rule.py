"""NAT Policy Rule Object Views."""

from nautobot.core.views import mixins

from nautobot_firewall_models.api.serializers import NATPolicyRuleSerializer
from nautobot_firewall_models.filters import NATPolicyRuleFilterSet
from nautobot_firewall_models.forms import NATPolicyRuleBulkEditForm, NATPolicyRuleFilterForm, NATPolicyRuleForm
from nautobot_firewall_models.models import NATPolicyRule
from nautobot_firewall_models.tables import NATPolicyRuleTable


class NATPolicyRuleUIViewSet(
    mixins.ObjectDetailViewMixin,
    mixins.ObjectListViewMixin,
    mixins.ObjectEditViewMixin,
    mixins.ObjectDestroyViewMixin,
    mixins.ObjectBulkDestroyViewMixin,
    mixins.ObjectBulkUpdateViewMixin,
):
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

    def _process_bulk_create_form(self, form):
        """Bulk creating (CSV import) is not supported."""
        raise NotImplementedError()
