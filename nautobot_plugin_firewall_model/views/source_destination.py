"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class SourceDestinationListView(generic.ObjectListView):
    """List view."""

    queryset = models.SourceDestination.objects.all()
    filterset = filters.SourceDestinationFilter
    filterset_form = forms.SourceDestinationFilterForm
    table = tables.SourceDestinationTable
    action_buttons = ("add",)


class SourceDestinationView(generic.ObjectView):
    """Detail view."""

    queryset = models.SourceDestination.objects.all()


class SourceDestinationCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.SourceDestination
    queryset = models.SourceDestination.objects.all()
    model_form = forms.SourceDestinationForm


class SourceDestinationDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.SourceDestination
    queryset = models.SourceDestination.objects.all()


class SourceDestinationEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.SourceDestination
    queryset = models.SourceDestination.objects.all()
    model_form = forms.SourceDestinationForm


class SourceDestinationBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more SourceDestination records."""

    queryset = models.SourceDestination.objects.all()
    table = tables.SourceDestinationTable


class SourceDestinationBulkEditView(generic.BulkEditView):
    """View for editing one or more SourceDestination records."""

    queryset = models.SourceDestination.objects.all()
    filterset = filters.SourceDestinationFilter
    table = tables.SourceDestinationTable
    form = forms.SourceDestinationBulkEditForm
