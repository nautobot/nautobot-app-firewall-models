"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class UserPolicyObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserPolicyObject.objects.all()
    filterset = filters.UserPolicyObjectFilterSet
    filterset_form = forms.UserPolicyObjectFilterForm
    table = tables.UserPolicyObjectTable
    action_buttons = ("add",)


class UserPolicyObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserPolicyObject.objects.all()


class UserPolicyObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.UserPolicyObject.objects.all()


class UserPolicyObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.UserPolicyObject.objects.all()
    model_form = forms.UserPolicyObjectForm


class UserPolicyObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserPolicyObject records."""

    queryset = models.UserPolicyObject.objects.all()
    table = tables.UserPolicyObjectTable


class UserPolicyObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more UserPolicyObject records."""

    queryset = models.UserPolicyObject.objects.all()
    filterset = filters.UserPolicyObjectFilterSet
    table = tables.UserPolicyObjectTable
    form = forms.UserPolicyObjectBulkEditForm
