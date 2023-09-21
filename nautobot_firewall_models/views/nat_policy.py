"""NATPolicy Object Views."""

from django.shortcuts import reverse, redirect
from django.views.generic.edit import CreateView

from nautobot_firewall_models import models


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
