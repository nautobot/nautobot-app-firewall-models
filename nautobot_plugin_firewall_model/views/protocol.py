"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class ProtocolListView(generic.ObjectListView):
    """List view."""

    queryset = models.Protocol.objects.all()
    filterset = filters.ProtocolFilter
    filterset_form = forms.ProtocolFilterForm
    table = tables.ProtocolTable
    action_buttons = ("add",)


class ProtocolView(generic.ObjectView):
    """Detail view."""

    queryset = models.Protocol.objects.all()


class ProtocolCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Protocol
    queryset = models.Protocol.objects.all()
    model_form = forms.ProtocolForm


class ProtocolDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Protocol
    queryset = models.Protocol.objects.all()


class ProtocolEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Protocol
    queryset = models.Protocol.objects.all()
    model_form = forms.ProtocolForm


class ProtocolBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Protocol records."""

    queryset = models.Protocol.objects.all()
    table = tables.ProtocolTable


class ProtocolBulkEditView(generic.BulkEditView):
    """View for editing one or more Protocol records."""

    queryset = models.Protocol.objects.all()
    filterset = filters.ProtocolFilter
    table = tables.ProtocolTable
    form = forms.ProtocolBulkEditForm
