"""IP Range Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class IPRangeListView(generic.ObjectListView):
    """List view."""

    queryset = models.IPRange.objects.all()
    filterset = filters.IPRangeFilterSet
    filterset_form = forms.IPRangeFilterForm
    table = tables.IPRangeTable
    action_buttons = ("add",)


class IPRangeView(generic.ObjectView):
    """Detail view."""

    queryset = models.IPRange.objects.all()


class IPRangeDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.IPRange.objects.all()


class IPRangeEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.IPRange.objects.all()
    model_form = forms.IPRangeForm


class IPRangeBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more IPRange records."""

    queryset = models.IPRange.objects.all()
    table = tables.IPRangeTable


class IPRangeBulkEditView(generic.BulkEditView):
    """View for editing one or more IPRange records."""

    queryset = models.IPRange.objects.all()
    filterset = filters.IPRangeFilterSet
    table = tables.IPRangeTable
    form = forms.IPRangeBulkEditForm
