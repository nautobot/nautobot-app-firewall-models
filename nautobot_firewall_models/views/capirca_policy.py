"""Views for Firewall models."""

from django.shortcuts import reverse, redirect
from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class CapircaPolicyListView(generic.ObjectListView):
    """List view."""

    queryset = models.CapircaPolicy.objects.all()
    filterset = filters.CapircaPolicyFilterSet
    filterset_form = forms.CapircaPolicyFilterForm
    table = tables.CapircaPolicyTable
    action_buttons = ()


class CapircaPolicyView(generic.ObjectView):
    """Detail view."""

    queryset = models.CapircaPolicy.objects.all()


class CapircaPolicyDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.CapircaPolicy.objects.all()


class CapircaPolicyEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.CapircaPolicy.objects.all()
    model_form = forms.CapircaPolicyForm


class CapircaPolicyBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more CapircaPolicy records."""

    queryset = models.CapircaPolicy.objects.all()
    table = tables.CapircaPolicyTable


class CapircaPolicyBulkEditView(generic.BulkEditView):
    """View for editing one or more CapircaPolicy records."""

    queryset = models.CapircaPolicy.objects.all()
    filterset = filters.CapircaPolicyFilterSet
    table = tables.CapircaPolicyTable
    form = forms.CapircaPolicyBulkEditForm
