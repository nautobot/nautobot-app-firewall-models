"""Role views."""
from nautobot.core.views import generic

from nautobot_firewall_models import models, filters, forms, tables


class RoleListView(generic.ObjectListView):
    """List view."""

    queryset = models.Role.objects.all()
    table = tables.RoleTable


class RoleView(generic.ObjectView):
    """Detail view."""

    queryset = models.Role.objects.all()


class RoleEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.Role.objects.all()
    model_form = forms.RoleForm


class RoleDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.Role.objects.all()


class RoleBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Policy records."""

    queryset = models.Role.objects.all()
    table = tables.RoleTable


class RoleBulkEditView(generic.BulkEditView):
    """View for editing one or more Role records."""

    queryset = models.Role.objects.all()
    filterset = filters.RoleFilterSet
    table = tables.RoleTable
    form = forms.RoleBulkEditForm
