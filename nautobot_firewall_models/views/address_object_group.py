"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class AddressObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.AddressObjectGroup.objects.all()
    filterset = filters.AddressObjectGroupFilterSet
    filterset_form = forms.AddressObjectGroupFilterForm
    table = tables.AddressObjectGroupTable
    action_buttons = ("add",)


class AddressObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.AddressObjectGroup.objects.all()


class AddressObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.AddressObjectGroup.objects.all()


class AddressObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.AddressObjectGroup.objects.all()
    model_form = forms.AddressObjectGroupForm


class AddressObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more AddressObjectGroup records."""

    queryset = models.AddressObjectGroup.objects.all()
    table = tables.AddressObjectGroupTable


class AddressObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more AddressObjectGroup records."""

    queryset = models.AddressObjectGroup.objects.all()
    filterset = filters.AddressObjectGroupFilterSet
    table = tables.AddressObjectGroupTable
    form = forms.AddressObjectGroupBulkEditForm
