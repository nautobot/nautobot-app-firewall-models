"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class FQDNListView(generic.ObjectListView):
    """List view."""

    queryset = models.FQDN.objects.all()
    filterset = filters.FQDNFilterSet
    filterset_form = forms.FQDNFilterForm
    table = tables.FQDNTable
    action_buttons = ("add",)


class FQDNView(generic.ObjectView):
    """Detail view."""

    queryset = models.FQDN.objects.all()


class FQDNDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.FQDN.objects.all()


class FQDNEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.FQDN.objects.all()
    model_form = forms.FQDNForm


class FQDNBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more FQDN records."""

    queryset = models.FQDN.objects.all()
    table = tables.FQDNTable


class FQDNBulkEditView(generic.BulkEditView):
    """View for editing one or more FQDN records."""

    queryset = models.FQDN.objects.all()
    filterset = filters.FQDNFilterSet
    table = tables.FQDNTable
    form = forms.FQDNBulkEditForm
