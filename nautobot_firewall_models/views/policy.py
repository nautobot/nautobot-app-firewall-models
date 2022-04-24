"""Views for Firewall models."""

from django.shortcuts import reverse, redirect
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

    queryset = models.Policy.objects.all()


class PolicyExpandedRulesView(generic.ObjectView):
    """Expanded Rules view."""

    queryset = models.Policy.objects.all().prefetch_related(
        "policyrulem2m_set__rule__service__service_objects",
        "policyrulem2m_set__rule__service__service_object_groups",
        "policyrulem2m_set__rule__source__address__address_objects",
        "policyrulem2m_set__rule__source__address__address_object_groups__address_objects",
        "policyrulem2m_set__rule__source__user__user_objects",
        "policyrulem2m_set__rule__source__user__user_object_groups__user_objects",
        "policyrulem2m_set__rule__source__zone",
        "policyrulem2m_set__rule__destination__zone",
        "policyrulem2m_set__rule__destination__address__address_objects",
        "policyrulem2m_set__rule__destination__address__address_object_groups__address_objects",
    )
    template_name = "nautobot_firewall_models/policy_expanded_rules.html"


class PolicyExpandedRulesIndexEditView(generic.ObjectView):
    """Expanded Rules view."""

    queryset = models.Policy.objects.all().prefetch_related(
        "policyrulem2m_set__rule__service__service_objects",
        "policyrulem2m_set__rule__service__service_object_groups",
        "policyrulem2m_set__rule__source__address__address_objects",
        "policyrulem2m_set__rule__source__address__address_object_groups__address_objects",
        "policyrulem2m_set__rule__source__user__user_objects",
        "policyrulem2m_set__rule__source__user__user_object_groups__user_objects",
        "policyrulem2m_set__rule__source__zone",
        "policyrulem2m_set__rule__destination__zone",
        "policyrulem2m_set__rule__destination__address__address_objects",
        "policyrulem2m_set__rule__destination__address__address_object_groups__address_objects",
    )
    template_name = "nautobot_firewall_models/assign_policy_rule_index.html"

    def post(self, request, pk, *args, **kwargs):
        # pylint: disable=C0103:
        """Method to set index on a rule in a policy."""
        form_data = dict(request.POST)
        form_data.pop("csrfmiddlewaretoken", None)
        for rule, index in form_data.items():
            m2m = models.PolicyRuleM2M.objects.get(rule=rule, policy=pk)
            m2m.index = index[0]
            m2m.validated_save()
        return redirect(reverse("plugins:nautobot_firewall_models:policy_policyrules", kwargs={"pk": pk}))


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
