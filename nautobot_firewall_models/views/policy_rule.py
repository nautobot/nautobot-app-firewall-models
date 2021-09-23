"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class PolicyRuleListView(generic.ObjectListView):
    """List view."""

    queryset = models.PolicyRule.objects.all()
    filterset = filters.PolicyRuleFilter
    filterset_form = forms.PolicyRuleFilterForm
    table = tables.PolicyRuleTable
    action_buttons = ("add",)


class PolicyRuleView(generic.ObjectView):
    """Detail view."""

    queryset = models.PolicyRule.objects.all()


class PolicyRuleCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.PolicyRule
    queryset = models.PolicyRule.objects.all()
    model_form = forms.PolicyRuleForm


class PolicyRuleDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.PolicyRule
    queryset = models.PolicyRule.objects.all()


class PolicyRuleEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.PolicyRule
    queryset = models.PolicyRule.objects.all()
    model_form = forms.PolicyRuleForm


class PolicyRuleBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more PolicyRule records."""

    queryset = models.PolicyRule.objects.all()
    table = tables.PolicyRuleTable


class PolicyRuleBulkEditView(generic.BulkEditView):
    """View for editing one or more PolicyRule records."""

    queryset = models.PolicyRule.objects.all()
    filterset = filters.PolicyRuleFilter
    table = tables.PolicyRuleTable
    form = forms.PolicyRuleBulkEditForm
