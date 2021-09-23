"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class AddressObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressObject.objects.all()
    filterset = filters.AddressObjectFilter
    filterset_form = forms.AddressObjectFilterForm
    table = tables.AddressObjectTable
    action_buttons = ("add",)


class AddressObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressObject.objects.all()


class AddressObjectCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.AddressObject
    queryset = models.AddressObject.objects.all()
    model_form = forms.AddressObjectForm


class AddressObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.AddressObject
    queryset = models.AddressObject.objects.all()


class AddressObjectEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.AddressObject
    queryset = models.AddressObject.objects.all()
    model_form = forms.AddressObjectForm


class AddressObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressObject records."""

    queryset = models.AddressObject.objects.all()
    table = tables.AddressObjectTable


class AddressObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressObject records."""

    queryset = models.AddressObject.objects.all()
    filterset = filters.AddressObjectFilter
    table = tables.AddressObjectTable
    form = forms.AddressObjectBulkEditForm
