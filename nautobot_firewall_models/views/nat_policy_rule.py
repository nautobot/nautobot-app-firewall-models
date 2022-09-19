"""NAT Policy Rule Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class NATPolicyRuleListView(generic.ObjectListView):
    """List view."""

    queryset = models.NATPolicyRule.objects.all()
    filterset = filters.NATPolicyRuleFilterSet
    filterset_form = forms.NATPolicyRuleFilterForm
    table = tables.NATPolicyRuleTable
    action_buttons = ("add",)


class NATPolicyRuleRuleView(generic.ObjectView):
    """Detail view."""

    queryset = models.NATPolicyRule.objects.all()


class NATPolicyRuleDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.NATPolicyRule.objects.all()


class NATPolicyRuleEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.NATPolicyRule.objects.all()
    model_form = forms.NATPolicyRuleForm


class NATPolicyRuleBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more NATPolicyRule records."""

    queryset = models.NATPolicyRule.objects.all()
    table = tables.NATPolicyRuleRuleTable


class NATPolicyRuleBulkEditView(generic.BulkEditView):
    """View for editing one or more NATPolicyRule records."""

    queryset = models.NATPolicyRule.objects.all()
    filterset = filters.NATPolicyRuleFilterSet
    table = tables.NATPolicyRuleTable
    form = forms.NATPolicyRuleBulkEditForm
