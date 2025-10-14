"""Service Object Viewsets."""

from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import details, filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class ApplicationObjectUIViewSet(NautobotUIViewSet):
    """ViewSet for the ApplicationObject model."""

    bulk_update_form_class = forms.ApplicationObjectBulkEditForm
    filterset_class = filters.ApplicationObjectFilterSet
    filterset_form_class = forms.ApplicationObjectFilterForm
    form_class = forms.ApplicationObjectForm
    queryset = models.ApplicationObject.objects.all()
    serializer_class = serializers.ApplicationObjectSerializer
    table_class = tables.ApplicationObjectTable
    object_detail_content = details.application_object

    lookup_field = "pk"


class ApplicationObjectGroupUIViewSet(NautobotUIViewSet):
    """ViewSet for the ApplicationObjectGroup model."""

    bulk_update_form_class = forms.ApplicationObjectGroupBulkEditForm
    filterset_class = filters.ApplicationObjectGroupFilterSet
    filterset_form_class = forms.ApplicationObjectGroupFilterForm
    form_class = forms.ApplicationObjectGroupForm
    queryset = models.ApplicationObjectGroup.objects.all()
    serializer_class = serializers.ApplicationObjectGroupSerializer
    table_class = tables.ApplicationObjectGroupTable
    object_detail_content = details.application_object_group

    lookup_field = "pk"


class ServiceObjectUIViewSet(NautobotUIViewSet):
    """ViewSet for the ServiceObject model."""

    bulk_update_form_class = forms.ServiceObjectBulkEditForm
    filterset_class = filters.ServiceObjectFilterSet
    filterset_form_class = forms.ServiceObjectFilterForm
    form_class = forms.ServiceObjectForm
    queryset = models.ServiceObject.objects.all()
    serializer_class = serializers.ServiceObjectSerializer
    table_class = tables.ServiceObjectTable
    object_detail_content = details.service_object

    lookup_field = "pk"


class ServiceObjectGroupUIViewSet(NautobotUIViewSet):
    """ViewSet for the ServiceObjectGroup model."""

    bulk_update_form_class = forms.ServiceObjectGroupBulkEditForm
    filterset_class = filters.ServiceObjectGroupFilterSet
    filterset_form_class = forms.ServiceObjectGroupFilterForm
    form_class = forms.ServiceObjectGroupForm
    queryset = models.ServiceObjectGroup.objects.all()
    serializer_class = serializers.ServiceObjectGroupSerializer
    table_class = tables.ServiceObjectGroupTable
    object_detail_content = details.service_object_group

    lookup_field = "pk"
