"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class PolicyRuleListView(generic.ObjectListView):
    """List view."""

    queryset = models.PolicyRule.objects.all()
    filterset = filters.PolicyRuleFilterSet
    filterset_form = forms.PolicyRuleFilterForm
    table = tables.PolicyRuleTable
    action_buttons = ("add",)


class PolicyRuleView(generic.ObjectView):
    """Detail view."""

    queryset = models.PolicyRule.objects.all()


class PolicyRuleDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.PolicyRule.objects.all()


class PolicyRuleEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.PolicyRule.objects.all()
    model_form = forms.PolicyRuleForm


class PolicyRuleBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more PolicyRule records."""

    queryset = models.PolicyRule.objects.all()
    table = tables.PolicyRuleTable


class PolicyRuleBulkEditView(generic.BulkEditView):
    """View for editing one or more PolicyRule records."""

    queryset = models.PolicyRule.objects.all()
    filterset = filters.PolicyRuleFilterSet
    table = tables.PolicyRuleTable
    form = forms.PolicyRuleBulkEditForm
