"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class UserGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserGroup.objects.all()
    filterset = filters.UserGroupFilter
    filterset_form = forms.UserGroupFilterForm
    table = tables.UserGroupTable
    action_buttons = ("add",)


class UserGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserGroup.objects.all()


class UserGroupCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.UserGroup
    queryset = models.UserGroup.objects.all()
    model_form = forms.UserGroupForm


class UserGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.UserGroup
    queryset = models.UserGroup.objects.all()


class UserGroupEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.UserGroup
    queryset = models.UserGroup.objects.all()
    model_form = forms.UserGroupForm


class UserGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserGroup records."""

    queryset = models.UserGroup.objects.all()
    table = tables.UserGroupTable


class UserGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more UserGroup records."""

    queryset = models.UserGroup.objects.all()
    filterset = filters.UserGroupFilter
    table = tables.UserGroupTable
    form = forms.UserGroupBulkEditForm
