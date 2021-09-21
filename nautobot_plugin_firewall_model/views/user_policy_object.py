"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class UserPolicyObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserPolicyObject.objects.all()
    filterset = filters.UserPolicyObjectFilter
    filterset_form = forms.UserPolicyObjectFilterForm
    table = tables.UserPolicyObjectTable
    action_buttons = ("add",)


class UserPolicyObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserPolicyObject.objects.all()


class UserPolicyObjectCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.UserPolicyObject
    queryset = models.UserPolicyObject.objects.all()
    model_form = forms.UserPolicyObjectForm


class UserPolicyObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.UserPolicyObject
    queryset = models.UserPolicyObject.objects.all()


class UserPolicyObjectEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.UserPolicyObject
    queryset = models.UserPolicyObject.objects.all()
    model_form = forms.UserPolicyObjectForm


class UserPolicyObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserPolicyObject records."""

    queryset = models.UserPolicyObject.objects.all()
    table = tables.UserPolicyObjectTable


class UserPolicyObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more UserPolicyObject records."""

    queryset = models.UserPolicyObject.objects.all()
    filterset = filters.UserPolicyObjectFilter
    table = tables.UserPolicyObjectTable
    form = forms.UserPolicyObjectBulkEditForm
