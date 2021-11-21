"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ServicePolicyObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServicePolicyObject.objects.all()
    filterset = filters.ServicePolicyObjectFilterSet
    filterset_form = forms.ServicePolicyObjectFilterForm
    table = tables.ServicePolicyObjectTable
    action_buttons = ("add",)


class ServicePolicyObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServicePolicyObject.objects.all()


class ServicePolicyObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.ServicePolicyObject.objects.all()


class ServicePolicyObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.ServicePolicyObject.objects.all()
    model_form = forms.ServicePolicyObjectForm


class ServicePolicyObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServicePolicyObject records."""

    queryset = models.ServicePolicyObject.objects.all()
    table = tables.ServicePolicyObjectTable


class ServicePolicyObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more ServicePolicyObject records."""

    queryset = models.ServicePolicyObject.objects.all()
    filterset = filters.ServicePolicyObjectFilterSet
    table = tables.ServicePolicyObjectTable
    form = forms.ServicePolicyObjectBulkEditForm
