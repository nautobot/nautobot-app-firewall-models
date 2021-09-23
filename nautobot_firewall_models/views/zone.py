"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ZoneListView(generic.ObjectListView):
    """List view."""

    queryset = models.Zone.objects.all()
    filterset = filters.ZoneFilter
    filterset_form = forms.ZoneFilterForm
    table = tables.ZoneTable
    action_buttons = ("add",)


class ZoneView(generic.ObjectView):
    """Detail view."""

    queryset = models.Zone.objects.all()


class ZoneCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Zone
    queryset = models.Zone.objects.all()
    model_form = forms.ZoneForm


class ZoneDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Zone
    queryset = models.Zone.objects.all()


class ZoneEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Zone
    queryset = models.Zone.objects.all()
    model_form = forms.ZoneForm


class ZoneBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Zone records."""

    queryset = models.Zone.objects.all()
    table = tables.ZoneTable


class ZoneBulkEditView(generic.BulkEditView):
    """View for editing one or more Zone records."""

    queryset = models.Zone.objects.all()
    filterset = filters.ZoneFilter
    table = tables.ZoneTable
    form = forms.ZoneBulkEditForm
