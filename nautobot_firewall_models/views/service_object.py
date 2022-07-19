"""Service Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ServiceObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceObject.objects.all()
    filterset = filters.ServiceObjectFilterSet
    filterset_form = forms.ServiceObjectFilterForm
    table = tables.ServiceObjectTable
    action_buttons = ("add",)


class ServiceObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceObject.objects.all()


class ServiceObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.ServiceObject.objects.all()


class ServiceObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.ServiceObject.objects.all()
    model_form = forms.ServiceObjectForm
    template_name = "nautobot_firewall_models/serviceobject_edit.html"


class ServiceObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceObject records."""

    queryset = models.ServiceObject.objects.all()
    table = tables.ServiceObjectTable


class ServiceObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceObject records."""

    queryset = models.ServiceObject.objects.all()
    filterset = filters.ServiceObjectFilterSet
    table = tables.ServiceObjectTable
    form = forms.ServiceObjectBulkEditForm
