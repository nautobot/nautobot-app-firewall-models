"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class UserObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.UserObject.objects.all()
    filterset = filters.UserObjectFilter
    filterset_form = forms.UserObjectFilterForm
    table = tables.UserObjectTable
    action_buttons = ("add",)


class UserObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.UserObject.objects.all()


class UserObjectCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.UserObject
    queryset = models.UserObject.objects.all()
    model_form = forms.UserObjectForm


class UserObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.UserObject
    queryset = models.UserObject.objects.all()


class UserObjectEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.UserObject
    queryset = models.UserObject.objects.all()
    model_form = forms.UserObjectForm


class UserObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more UserObject records."""

    queryset = models.UserObject.objects.all()
    table = tables.UserObjectTable


class UserObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more UserObject records."""

    queryset = models.UserObject.objects.all()
    filterset = filters.UserObjectFilter
    table = tables.UserObjectTable
    form = forms.UserObjectBulkEditForm
