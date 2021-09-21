"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class SourceListView(generic.ObjectListView):
    """List view."""

    queryset = models.Source.objects.all()
    filterset = filters.SourceFilter
    filterset_form = forms.SourceFilterForm
    table = tables.SourceTable
    action_buttons = ("add",)


class SourceView(generic.ObjectView):
    """Detail view."""

    queryset = models.Source.objects.all()


class SourceCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Source
    queryset = models.Source.objects.all()
    model_form = forms.SourceForm


class SourceDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Source
    queryset = models.Source.objects.all()


class SourceEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Source
    queryset = models.Source.objects.all()
    model_form = forms.SourceForm


class SourceBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Source records."""

    queryset = models.Source.objects.all()
    table = tables.SourceTable


class SourceBulkEditView(generic.BulkEditView):
    """View for editing one or more Source records."""

    queryset = models.Source.objects.all()
    filterset = filters.SourceFilter
    table = tables.SourceTable
    form = forms.SourceBulkEditForm
