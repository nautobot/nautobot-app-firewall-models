"""User Object Views."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class UserObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserObject.objects.all()
    filterset = filters.UserObjectFilterSet
    filterset_form = forms.UserObjectFilterForm
    table = tables.UserObjectTable
    action_buttons = ("add",)


class UserObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserObject.objects.all()


class UserObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.UserObject.objects.all()


class UserObjectEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.UserObject.objects.all()
    model_form = forms.UserObjectForm


class UserObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserObject records."""

    queryset = models.UserObject.objects.all()
    table = tables.UserObjectTable


class UserObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more UserObject records."""

    queryset = models.UserObject.objects.all()
    filterset = filters.UserObjectFilterSet
    table = tables.UserObjectTable
    form = forms.UserObjectBulkEditForm
