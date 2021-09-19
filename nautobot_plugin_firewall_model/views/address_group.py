"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class AddressGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressGroup.objects.all()
    filterset = filters.AddressGroupFilter
    filterset_form = forms.AddressGroupFilterForm
    table = tables.AddressGroupTable
    action_buttons = ("add",)


class AddressGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressGroup.objects.all()


class AddressGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.AddressGroup
    queryset = models.AddressGroup.objects.all()
    model_form = forms.AddressGroupForm


class AddressGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.AddressGroup
    queryset = models.AddressGroup.objects.all()


class AddressGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.AddressGroup
    queryset = models.AddressGroup.objects.all()
    model_form = forms.AddressGroupForm


class AddressGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressGroup records."""

    queryset = models.AddressGroup.objects.all()
    table = tables.AddressGroupTable


class AddressGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressGroup records."""

    queryset = models.AddressGroup.objects.all()
    filterset = filters.AddressGroupFilter
    table = tables.AddressGroupTable
    form = forms.AddressGroupBulkEditForm
