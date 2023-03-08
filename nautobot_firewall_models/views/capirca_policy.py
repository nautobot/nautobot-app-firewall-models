"""Capirca Views."""

from django.shortcuts import render

from nautobot.core.views import generic
from nautobot.dcim.models import Device
from nautobot.core.views.mixins import ContentTypePermissionRequiredMixin

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


# CapircaPolicy Non-Standards


class CapircaPolicyDeviceView(ContentTypePermissionRequiredMixin, generic.View):
    """View for individual device detailed information."""

    def get_required_permission(self):
        """Manually set permission when not tied to a model for device report."""
        return "nautobot_firewall_models.view_capircapolicy"

    def get(self, request, pk):  # pylint: disable=invalid-name
        """Read request into a view of a single device."""
        device = Device.objects.get(pk=pk)
        compliance_details = models.CapircaPolicy.objects.get(device=device)

        config_details = {"object": compliance_details, "device": device}

        return render(
            request,
            "nautobot_firewall_models/capircapolicy_details.html",
            config_details,
        )
