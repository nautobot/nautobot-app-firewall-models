"""Views for nautobot_firewall_models."""

from nautobot.apps.ui import ObjectDetailContent, ObjectFieldsPanel, SectionChoices
from nautobot.apps.views import NautobotUIViewSet

from nautobot_firewall_models import filters, forms, models, tables
from nautobot_firewall_models.api import serializers


class IPRangeUIViewSet(NautobotUIViewSet):
    """ViewSet for IPRange views."""

    bulk_update_form_class = forms.IPRangeBulkEditForm
    filterset_class = filters.IPRangeFilterSet
    filterset_form_class = forms.IPRangeFilterForm
    form_class = forms.IPRangeForm
    lookup_field = "pk"
    queryset = models.IPRange.objects.all()
    serializer_class = serializers.IPRangeSerializer
    table_class = tables.IPRangeTable

    # Here is an example of using the UI  Component Framework for the detail view.
    # More information can be found in the Nautobot documentation:
    # https://docs.nautobot.com/projects/core/en/stable/development/core/ui-component-framework/
    object_detail_content = ObjectDetailContent(
        panels=[
            ObjectFieldsPanel(
                weight=100,
                section=SectionChoices.LEFT_HALF,
                fields="__all__",
                # Alternatively, you can specify a list of field names:
                # fields=[
                #     "name",
                #     "description",
                # ],
                # Some fields may require additional configuration, we can use value_transforms
                # value_transforms={
                #     "name": [helpers.bettertitle]
                # },
            ),
            # If there is a ForeignKey or M2M with this model we can use ObjectsTablePanel
            # to display them in a table format.
            # ObjectsTablePanel(
            # weight=200,
            # section=SectionChoices.RIGHT_HALF,
            # table_class=tables.IPRangeTable,
            # You will want to filter the table using the related_name
            # filter="ipranges",
            # ),
        ],
    )
