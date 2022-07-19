"""User Group Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class UserObjectGroupListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserObjectGroup.objects.all()
    filterset = filters.UserObjectGroupFilterSet
    filterset_form = forms.UserObjectGroupFilterForm
    table = tables.UserObjectGroupTable
    action_buttons = ("add",)


class UserObjectGroupView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserObjectGroup.objects.all()


class UserObjectGroupDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.UserObjectGroup.objects.all()


class UserObjectGroupEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.UserObjectGroup.objects.all()
    model_form = forms.UserObjectGroupForm


class UserObjectGroupBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserObjectGroup records."""

    queryset = models.UserObjectGroup.objects.all()
    table = tables.UserObjectGroupTable


class UserObjectGroupBulkEditView(generic.BulkEditView):
    """View for editing one or more UserObjectGroup records."""

    queryset = models.UserObjectGroup.objects.all()
    filterset = filters.UserObjectGroupFilterSet
    table = tables.UserObjectGroupTable
    form = forms.UserObjectGroupBulkEditForm
