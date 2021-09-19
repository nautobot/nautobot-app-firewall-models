"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class ServiceGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServiceGroup.objects.all()
    filterset = filters.ServiceGroupFilter
    filterset_form = forms.ServiceGroupFilterForm
    table = tables.ServiceGroupTable
    action_buttons = ("add",)


class ServiceGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServiceGroup.objects.all()


class ServiceGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()
    model_form = forms.ServiceGroupForm


class ServiceGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()


class ServiceGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServiceGroup
    queryset = models.ServiceGroup.objects.all()
    model_form = forms.ServiceGroupForm


class ServiceGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServiceGroup records."""

    queryset = models.ServiceGroup.objects.all()
    table = tables.ServiceGroupTable


class ServiceGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more ServiceGroup records."""

    queryset = models.ServiceGroup.objects.all()
    filterset = filters.ServiceGroupFilter
    table = tables.ServiceGroupTable
    form = forms.ServiceGroupBulkEditForm
