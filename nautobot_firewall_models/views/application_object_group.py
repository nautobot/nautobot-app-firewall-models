"""Application Object Group Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ApplicationObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.ApplicationObjectGroup.objects.all()
    filterset = filters.ApplicationObjectGroupFilterSet
    filterset_form = forms.ApplicationObjectGroupFilterForm
    table = tables.ApplicationObjectGroupTable
    action_buttons = ("add",)


class ApplicationObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.ApplicationObjectGroup.objects.all()


class ApplicationObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.ApplicationObjectGroup.objects.all()


class ApplicationObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.ApplicationObjectGroup.objects.all()
    model_form = forms.ApplicationObjectGroupForm


class ApplicationObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ApplicationObjectGroup records."""

    queryset = models.ApplicationObjectGroup.objects.all()
    table = tables.ApplicationObjectGroupTable


class ApplicationObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more ApplicationObjectGroup records."""

    queryset = models.ApplicationObjectGroup.objects.all()
    filterset = filters.ApplicationObjectGroupFilterSet
    table = tables.ApplicationObjectGroupTable
    form = forms.ApplicationObjectGroupBulkEditForm
