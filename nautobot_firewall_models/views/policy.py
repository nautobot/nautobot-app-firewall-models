"""Policy Object Views."""

from django.shortcuts import reverse, redirect
from django.views.generic.edit import CreateView
from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class PolicyListView(generic.ObjectListView):
    """List view."""

    queryset = models.Policy.objects.all()
    filterset = filters.PolicyFilterSet
    filterset_form = forms.PolicyFilterForm
    table = tables.PolicyTable
    action_buttons = ("add",)


class PolicyView(generic.ObjectView):
    """Detail view."""

    queryset = models.Policy.objects.all().prefetch_related(
        "policyrulem2m_set__rule__source_addresses",
        "policyrulem2m_set__rule__source_address_groups",
        "policyrulem2m_set__rule__source_users",
        "policyrulem2m_set__rule__source_user_groups",
        "policyrulem2m_set__rule__source_zone",
        "policyrulem2m_set__rule__source_services",
        "policyrulem2m_set__rule__source_service_groups",
        "policyrulem2m_set__rule__destination_zone",
        "policyrulem2m_set__rule__destination_addresses",
        "policyrulem2m_set__rule__destination_address_groups",
        "policyrulem2m_set__rule__destination_services",
        "policyrulem2m_set__rule__destination_service_groups",
    )


class PolicyDynamicGroupWeight(CreateView):
    """View to set weight on a DynamicGroup/Policy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = models.PolicyDynamicGroupM2M.objects.get(dynamic_group=group, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))


class PolicyDeviceWeight(CreateView):
    """View to set weight on a Device/Policy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = models.PolicyDeviceM2M.objects.get(device=device, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy", kwargs={"pk": pk}))


class PolicyDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.Policy.objects.all()


class PolicyEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.Policy.objects.all()
    model_form = forms.PolicyForm


class PolicyBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Policy records."""

    queryset = models.Policy.objects.all()
    table = tables.PolicyTable


class PolicyBulkEditView(generic.BulkEditView):
    """View for editing one or more Policy records."""

    queryset = models.Policy.objects.all()
    filterset = filters.PolicyFilterSet
    table = tables.PolicyTable
    form = forms.PolicyBulkEditForm
