"""NATPolicy Object Views."""

from django.shortcuts import reverse, redirect
from django.views.generic.edit import CreateView
from nautobot.core.views import generic

from nautobot_firewall_models import filters, forms, models, tables


class NATPolicyListView(generic.ObjectListView):
    """List view."""

    queryset = models.NATPolicy.objects.all()
    filterset = filters.NATPolicyFilterSet
    filterset_form = forms.NATPolicyFilterForm
    table = tables.NATPolicyTable
    action_buttons = ("add",)


class NATPolicyView(generic.ObjectView):
    """Detail view."""

    # TODO: This is incorrect.
    queryset = models.NATPolicy.objects.all().prefetch_related(
        "natpolicyrulem2m_set__rule__source_addresses",
        "natpolicyrulem2m_set__rule__source_address_groups",
        "natpolicyrulem2m_set__rule__source_users",
        "natpolicyrulem2m_set__rule__source_user_groups",
        "natpolicyrulem2m_set__rule__source_zone",
        "natpolicyrulem2m_set__rule__source_services",
        "natpolicyrulem2m_set__rule__source_service_groups",
        "natpolicyrulem2m_set__rule__destination_zone",
        "natpolicyrulem2m_set__rule__destination_addresses",
        "natpolicyrulem2m_set__rule__destination_address_groups",
        "natpolicyrulem2m_set__rule__destination_services",
        "natpolicyrulem2m_set__rule__destination_service_groups",
    )


class NATPolicyDynamicGroupWeight(CreateView):
    """View to set weight on a DynamicGroup/NATPolicy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a DynamicGroup & Policy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for group, weight in form_data.items():
            m2m = models.NATPolicyDynamicGroupM2M.objects.get(dynamic_group=group, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:nat_policy", kwargs={"pk": pk}))


class NATPolicyDeviceWeight(CreateView):
    """View to set weight on a Device/NATPolicy relationship."""

    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=invalid-name, arguments-differ
        """Method to set weight on a Device & NATPolicy Relationship."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for device, weight in form_data.items():
            m2m = models.NATPolicyDeviceM2M.objects.get(device=device, policy=pk)
            m2m.weight = weight[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:nat_policy", kwargs={"pk": pk}))


class NATPolicyDeleteView(generic.ObjectDeleteView):
    """Delete view."""

    queryset = models.NATPolicy.objects.all()


class NATPolicyEditView(generic.ObjectEditView):
    """Edit view."""

    queryset = models.NATPolicy.objects.all()
    model_form = forms.NATPolicyForm


class NATPolicyBulkDeleteView(generic.BulkDeleteView):
    """View for deleting one or more Policy records."""

    queryset = models.NATPolicy.objects.all()
    table = tables.NATPolicyTable


class NATPolicyBulkEditView(generic.BulkEditView):
    """View for editing one or more Policy records."""

    queryset = models.NATPolicy.objects.all()
    filterset = filters.NATPolicyFilterSet
    table = tables.NATPolicyTable
    form = forms.NATPolicyBulkEditForm
