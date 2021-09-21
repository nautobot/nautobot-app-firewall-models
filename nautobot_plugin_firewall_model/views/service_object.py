"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class ServiceObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceObject.objects.all()
    filterset = filters.ServiceObjectFilter
    filterset_form = forms.ServiceObjectFilterForm
    table = tables.ServiceObjectTable
    action_buttons = ("add",)


class ServiceObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceObject.objects.all()


class ServiceObjectCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceObject
    queryset = models.ServiceObject.objects.all()
    model_form = forms.ServiceObjectForm


class ServiceObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceObject
    queryset = models.ServiceObject.objects.all()


class ServiceObjectEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceObject
    queryset = models.ServiceObject.objects.all()
    model_form = forms.ServiceObjectForm


class ServiceObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceObject records."""

    queryset = models.ServiceObject.objects.all()
    table = tables.ServiceObjectTable


class ServiceObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceObject records."""

    queryset = models.ServiceObject.objects.all()
    filterset = filters.ServiceObjectFilter
    table = tables.ServiceObjectTable
    form = forms.ServiceObjectBulkEditForm
