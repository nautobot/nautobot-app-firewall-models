"""Views for Firewall models."""

from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class ServicePolicyObjectListView(generic.ObjectListView):
    """List view."""

    queryset = models.ServicePolicyObject.objects.all()
    filterset = filters.ServicePolicyObjectFilter
    filterset_form = forms.ServicePolicyObjectFilterForm
    table = tables.ServicePolicyObjectTable
    action_buttons = ("add",)


class ServicePolicyObjectView(generic.ObjectView):
    """Detail view."""

    queryset = models.ServicePolicyObject.objects.all()


class ServicePolicyObjectCreateView(generic.ObjectEditView):
    """Create view."""

    model = models.ServicePolicyObject
    queryset = models.ServicePolicyObject.objects.all()
    model_form = forms.ServicePolicyObjectForm


class ServicePolicyObjectDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    model = models.ServicePolicyObject
    queryset = models.ServicePolicyObject.objects.all()


class ServicePolicyObjectEditView(generic.ObjectEditView):
    """Edit view."""

    model = models.ServicePolicyObject
    queryset = models.ServicePolicyObject.objects.all()
    model_form = forms.ServicePolicyObjectForm


class ServicePolicyObjectBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more ServicePolicyObject records."""

    queryset = models.ServicePolicyObject.objects.all()
    table = tables.ServicePolicyObjectTable


class ServicePolicyObjectBulkEditView(generic.BulkEditView):
    """View for editing one or more ServicePolicyObject records."""

    queryset = models.ServicePolicyObject.objects.all()
    filterset = filters.ServicePolicyObjectFilter
    table = tables.ServicePolicyObjectTable
    form = forms.ServicePolicyObjectBulkEditForm
