"""User Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class UserObjectUIViewSet(NautobotUIViewSet):
    """ViewSet for the UserObject model."""

    bulk_update_form_class = forms.UserObjectBulkEditForm
    filterset_class = filters.UserObjectFilterSet
    filterset_form_class = forms.UserObjectFilterForm
    form_class = forms.UserObjectForm
    queryset = models.UserObject.objects.all()
    serializer_class = serializers.UserObjectSerializer
    table_class = tables.UserObjectTable
    action_buttons = ("add",)

    lookup_field = "pk"


class UserObjectGroupUIViewSet(NautobotUIViewSet):
    """ViewSet for the UserObjectGroup model."""

    bulk_update_form_class = forms.UserObjectGroupBulkEditForm
    filterset_class = filters.UserObjectGroupFilterSet
    filterset_form_class = forms.UserObjectGroupFilterForm
    form_class = forms.UserObjectGroupForm
    queryset = models.UserObjectGroup.objects.all()
    serializer_class = serializers.UserObjectGroupSerializer
    table_class = tables.UserObjectGroupTable
    action_buttons = ("add",)

    lookup_field = "pk"
