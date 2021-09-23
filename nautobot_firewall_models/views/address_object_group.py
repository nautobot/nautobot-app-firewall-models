"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class AddressObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressObjectGroup.objects.all()
    filterset = filters.AddressObjectGroupFilter
    filterset_form = forms.AddressObjectGroupFilterForm
    table = tables.AddressObjectGroupTable
    action_buttons = ("add",)


class AddressObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressObjectGroup.objects.all()


class AddressObjectGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.AddressObjectGroup
    queryset = models.AddressObjectGroup.objects.all()
    model_form = forms.AddressObjectGroupForm


class AddressObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.AddressObjectGroup
    queryset = models.AddressObjectGroup.objects.all()


class AddressObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.AddressObjectGroup
    queryset = models.AddressObjectGroup.objects.all()
    model_form = forms.AddressObjectGroupForm


class AddressObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressObjectGroup records."""

    queryset = models.AddressObjectGroup.objects.all()
    table = tables.AddressObjectGroupTable


class AddressObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressObjectGroup records."""

    queryset = models.AddressObjectGroup.objects.all()
    filterset = filters.AddressObjectGroupFilter
    table = tables.AddressObjectGroupTable
    form = forms.AddressObjectGroupBulkEditForm
