"""Service Group Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ServiceObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceObjectGroup.objects.all()
    filterset = filters.ServiceObjectGroupFilterSet
    filterset_form = forms.ServiceObjectGroupFilterForm
    table = tables.ServiceObjectGroupTable
    action_buttons = ("add",)


class ServiceObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceObjectGroup.objects.all()


class ServiceObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.ServiceObjectGroup.objects.all()


class ServiceObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.ServiceObjectGroup.objects.all()
    model_form = forms.ServiceObjectGroupForm


class ServiceObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceObjectGroup records."""

    queryset = models.ServiceObjectGroup.objects.all()
    table = tables.ServiceObjectGroupTable


class ServiceObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceObjectGroup records."""

    queryset = models.ServiceObjectGroup.objects.all()
    filterset = filters.ServiceObjectGroupFilterSet
    table = tables.ServiceObjectGroupTable
    form = forms.ServiceObjectGroupBulkEditForm
