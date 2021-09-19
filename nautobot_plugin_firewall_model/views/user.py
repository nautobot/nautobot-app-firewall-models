"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_plugin_firewall_model import filters, forms, models, tables


class UserListView(generic.ObjectListView):
    """List view."""

    queryset = models.User.objects.all()
    filterset = filters.UserFilter
    filterset_form = forms.UserFilterForm
    table = tables.UserTable
    action_buttons = ("add",)


class UserView(generic.ObjectView):
    """Detail view."""

    queryset = models.User.objects.all()


class UserCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.User
    queryset = models.User.objects.all()
    model_form = forms.UserForm


class UserDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.User
    queryset = models.User.objects.all()


class UserEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.User
    queryset = models.User.objects.all()
    model_form = forms.UserForm


class UserBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more User records."""

    queryset = models.User.objects.all()
    table = tables.UserTable


class UserBulkEditView(generic.BulkEditView):
    """View for editing one or more User records."""

    queryset = models.User.objects.all()
    filterset = filters.UserFilter
    table = tables.UserTable
    form = forms.UserBulkEditForm
