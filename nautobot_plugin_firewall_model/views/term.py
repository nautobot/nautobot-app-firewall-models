"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class TermListView(generic.ObjectListView):
    """List view."""

    queryset = models.Term.objects.all()
    filterset = filters.TermFilter
    filterset_form = forms.TermFilterForm
    table = tables.TermTable
    action_buttons = ("add",)


class TermView(generic.ObjectView):
    """Detail view."""

    queryset = models.Term.objects.all()


class TermCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.Term
    queryset = models.Term.objects.all()
    model_form = forms.TermForm


class TermDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.Term
    queryset = models.Term.objects.all()


class TermEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.Term
    queryset = models.Term.objects.all()
    model_form = forms.TermForm


class TermBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Term records."""

    queryset = models.Term.objects.all()
    table = tables.TermTable


class TermBulkEditView(generic.BulkEditView):
    """View for editing one or more Term records."""

    queryset = models.Term.objects.all()
    filterset = filters.TermFilter
    table = tables.TermTable
    form = forms.TermBulkEditForm
