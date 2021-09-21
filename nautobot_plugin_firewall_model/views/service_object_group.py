"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class ServiceObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceObjectGroup.objects.all()
    filterset = filters.ServiceObjectGroupFilter
    filterset_form = forms.ServiceObjectGroupFilterForm
    table = tables.ServiceObjectGroupTable
    action_buttons = ("add",)


class ServiceObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceObjectGroup.objects.all()


class ServiceObjectGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceObjectGroup
    queryset = models.ServiceObjectGroup.objects.all()
    model_form = forms.ServiceObjectGroupForm


class ServiceObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceObjectGroup
    queryset = models.ServiceObjectGroup.objects.all()


class ServiceObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceObjectGroup
    queryset = models.ServiceObjectGroup.objects.all()
    model_form = forms.ServiceObjectGroupForm


class ServiceObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceObjectGroup records."""

    queryset = models.ServiceObjectGroup.objects.all()
    table = tables.ServiceObjectGroupTable


class ServiceObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceObjectGroup records."""

    queryset = models.ServiceObjectGroup.objects.all()
    filterset = filters.ServiceObjectGroupFilter
    table = tables.ServiceObjectGroupTable
    form = forms.ServiceObjectGroupBulkEditForm
