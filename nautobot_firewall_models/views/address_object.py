"""Address Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class AddressObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressObject.objects.all()
    filterset = filters.AddressObjectFilterSet
    filterset_form = forms.AddressObjectFilterForm
    table = tables.AddressObjectTable
    action_buttons = ("add",)


class AddressObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressObject.objects.all()


class AddressObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.AddressObject.objects.all()


class AddressObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.AddressObject.objects.all()
    model_form = forms.AddressObjectForm


class AddressObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressObject records."""

    queryset = models.AddressObject.objects.all()
    table = tables.AddressObjectTable


class AddressObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressObject records."""

    queryset = models.AddressObject.objects.all()
    filterset = filters.AddressObjectFilterSet
    table = tables.AddressObjectTable
    form = forms.AddressObjectBulkEditForm
