"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class DestinationListView(generic.ObjectListView):
    """List view."""

    queryset = models.Destination.objects.all()
    filterset = filters.DestinationFilter
    filterset_form = forms.DestinationFilterForm
    table = tables.DestinationTable
    action_buttons = ("add",)


class DestinationView(generic.ObjectView):
    """Detail view."""

    queryset = models.Destination.objects.all()


class DestinationCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Destination
    queryset = models.Destination.objects.all()
    model_form = forms.DestinationForm


class DestinationDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Destination
    queryset = models.Destination.objects.all()


class DestinationEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Destination
    queryset = models.Destination.objects.all()
    model_form = forms.DestinationForm


class DestinationBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Destination records."""

    queryset = models.Destination.objects.all()
    table = tables.DestinationTable


class DestinationBulkEditView(generic.BulkEditView):
    """View for editing one or more Destination records."""

    queryset = models.Destination.objects.all()
    filterset = filters.DestinationFilter
    table = tables.DestinationTable
    form = forms.DestinationBulkEditForm
