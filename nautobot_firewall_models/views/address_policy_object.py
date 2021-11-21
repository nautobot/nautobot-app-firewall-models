"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class AddressPolicyObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressPolicyObject.objects.all()
    filterset = filters.AddressPolicyObjectFilterSet
    filterset_form = forms.AddressPolicyObjectFilterForm
    table = tables.AddressPolicyObjectTable
    action_buttons = ("add",)


class AddressPolicyObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressPolicyObject.objects.all()


class AddressPolicyObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.AddressPolicyObject.objects.all()


class AddressPolicyObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.AddressPolicyObject.objects.all()
    model_form = forms.AddressPolicyObjectForm


class AddressPolicyObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressPolicyObject records."""

    queryset = models.AddressPolicyObject.objects.all()
    table = tables.AddressPolicyObjectTable


class AddressPolicyObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressPolicyObject records."""

    queryset = models.AddressPolicyObject.objects.all()
    filterset = filters.AddressPolicyObjectFilterSet
    table = tables.AddressPolicyObjectTable
    form = forms.AddressPolicyObjectBulkEditForm
