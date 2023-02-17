"""Application Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ApplicationObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.ApplicationObject.objects.all()
    filterset = filters.ApplicationObjectFilterSet
    filterset_form = forms.ApplicationObjectFilterForm
    table = tables.ApplicationObjectTable
    action_buttons = ("add",)


class ApplicationObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.ApplicationObject.objects.all()


class ApplicationObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.ApplicationObject.objects.all()


class ApplicationObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.ApplicationObject.objects.all()
    model_form = forms.ApplicationObjectForm


class ApplicationObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ApplicationObject records."""

    queryset = models.ApplicationObject.objects.all()
    table = tables.ApplicationObjectTable


class ApplicationObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more ApplicationObject records."""

    queryset = models.ApplicationObject.objects.all()
    filterset = filters.ApplicationObjectFilterSet
    table = tables.ApplicationObjectTable
    form = forms.ApplicationObjectBulkEditForm
