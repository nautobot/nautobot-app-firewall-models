"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class SourceListView(generic.ObjectListView):
    """List view."""

    queryset = models.Source.objects.all()
    filterset = filters.SourceFilterSet
    filterset_form = forms.SourceFilterForm
    table = tables.SourceTable
    action_buttons = ("add",)


class SourceView(generic.ObjectView):
    """Detail view."""

    queryset = models.Source.objects.all()


class SourceDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.Source.objects.all()


class SourceEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.Source.objects.all()
    model_form = forms.SourceForm


class SourceBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Source records."""

    queryset = models.Source.objects.all()
    table = tables.SourceTable


class SourceBulkEditView(generic.BulkEditView):
    """View for editing one or more Source records."""

    queryset = models.Source.objects.all()
    filterset = filters.SourceFilterSet
    table = tables.SourceTable
    form = forms.SourceBulkEditForm
