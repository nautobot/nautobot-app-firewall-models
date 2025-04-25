"""Forms for nautobot_firewall_models."""

from django import forms
from nautobot.apps.forms import NautobotBulkEditForm, NautobotFilterForm, NautobotModelForm, TagsBulkEditFormMixin

from nautobot_firewall_models import models


class IPRangeForm(NautobotModelForm):  # pylint: disable=too-many-ancestors
    """IPRange creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = "__all__"


class IPRangeBulkEditForm(TagsBulkEditFormMixin, NautobotBulkEditForm):  # pylint: disable=too-many-ancestors
    """IPRange bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.IPRange.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class IPRangeFilterForm(NautobotFilterForm):
    """Filter form to filter searches."""

    model = models.IPRange
    field_order = ["q", "name"]

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name.",
    )
    name = forms.CharField(required=False, label="Name")
