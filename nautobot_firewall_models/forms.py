"""Forms for the Firewall plugin."""

from django import forms
from nautobot.dcim.models import Interface
from nautobot.extras.forms import (
    AddRemoveTagsForm,
    StatusFilterFormMixin,
    StatusBulkEditFormMixin,
    CustomFieldFilterForm,
)
from nautobot.extras.models import Tag
from nautobot.ipam.models import VRF, Prefix, IPAddress
from nautobot.utilities.forms import (
    BootstrapMixin,
    BulkEditForm,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)

from nautobot_firewall_models import models, fields, choices


class IPRangeFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.IPRange
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    start_address = forms.CharField(required=False, label="Starting Address")
    end_address = forms.CharField(required=False, label="Ending Address")
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)


class IPRangeForm(BootstrapMixin, fields.IPRangeFieldMixin, forms.ModelForm):
    """IPRange creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["vrf", "description", "status"]


class IPRangeBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """IPRange bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.IPRange.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    # start_address = forms.CharField(required=False)
    # end_address = forms.CharField(required=False)
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrf"]


class FQDNFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.FQDN
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class FQDNForm(BootstrapMixin, forms.ModelForm):
    """FQDN creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["name", "description", "ip_addresses", "status"]


class FQDNBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """FQDN bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.FQDN.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "ip_addresses"]


class AddressObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.AddressObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="IP Address")
    ip_range = DynamicModelChoiceField(queryset=models.IPRange.objects.all(), required=False, label="IP Range")
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False, label="Prefix")
    fqdn = DynamicModelChoiceField(queryset=models.FQDN.objects.all(), required=False, label="FQDN")


class AddressObjectForm(BootstrapMixin, forms.ModelForm):
    """AddressObject creation/edit form."""

    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="IP Address")
    ip_range = DynamicModelChoiceField(queryset=models.IPRange.objects.all(), required=False, label="IP Range")
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False, label="Prefix")
    fqdn = DynamicModelChoiceField(queryset=models.FQDN.objects.all(), required=False, label="FQDN")

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = ["name", "description", "fqdn", "ip_range", "ip_address", "prefix", "status"]


class AddressObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """AddressObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.AddressObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectGroupFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.AddressObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class AddressObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """AddressObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = ["name", "description", "address_objects", "status"]


class AddressObjectGroupBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """AddressObjectGroup bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class AddressPolicyObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.AddressPolicyObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class AddressPolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """AddressPolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = ["name", "description", "address_objects", "address_object_groups", "status"]


class AddressPolicyObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """AddressPolicyObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.AddressPolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "address_objects", "address_object_groups"]


class ServiceObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.ServiceObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    port = forms.IntegerField(required=False)
    ip_protocol = forms.ChoiceField(choices=choices.IP_PROTOCOL_CHOICES)


class ServiceObjectForm(BootstrapMixin, forms.ModelForm):
    """ServiceObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = ["name", "description", "port", "ip_protocol", "status"]


class ServiceObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """ServiceObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "port", "ip_protocol"]


class ServiceObjectGroupFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.ServiceObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class ServiceObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """ServiceObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ["name", "description", "service_objects", "status"]


class ServiceObjectGroupBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """ServiceObjectGroup bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ServicePolicyObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.ServicePolicyObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class ServicePolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """ServicePolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = ["name", "description", "service_objects", "service_object_groups", "status"]


class ServicePolicyObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """ServicePolicyObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.ServicePolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "service_objects", "service_object_groups"]


class UserObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.UserObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    username = forms.CharField(required=False, label="Username")


class UserObjectForm(BootstrapMixin, forms.ModelForm):
    """UserObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = ["username", "name", "status"]


class UserObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """UserObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "name",
        ]


class UserObjectGroupFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.UserObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class UserObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """UserObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ["name", "description", "user_objects", "status"]


class UserObjectGroupBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """UserObjectGroup bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.UserObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class UserPolicyObjectFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.UserPolicyObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class UserPolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """UserPolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = ["name", "description", "user_objects", "user_object_groups", "status"]


class UserPolicyObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """UserPolicyObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.UserPolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "user_objects", "user_object_groups"]


class ZoneFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.Zone
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    vrfs = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF")
    interfaces = DynamicModelChoiceField(queryset=Interface.objects.all(), label="Interface")


class ZoneForm(BootstrapMixin, forms.ModelForm):
    """Zone creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = ["name", "description", "vrfs", "interfaces", "status"]


class ZoneBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """Zone bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Zone.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    interfaces = DynamicModelMultipleChoiceField(queryset=Interface.objects.all(), required=False, label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


class SourceDestinationFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.SourceDestination
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    display = forms.CharField(required=False, label="Display")


class SourceDestinationForm(BootstrapMixin, forms.ModelForm):
    """SourceDestination creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.SourceDestination
        fields = ["description", "address", "service", "user", "zone", "status"]


class SourceDestinationBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """SourceDestination bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.SourceDestination.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "user", "zone"]


class PolicyRuleFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.PolicyRule
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="name")
    tag = TagFilterField(models.PolicyRule)


class PolicyRuleForm(BootstrapMixin, forms.ModelForm):
    """PolicyRule creation/edit form."""

    name = forms.CharField(required=False, label="Name")
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = ["name", "index", "action", "log", "source", "destination", "tags", "status"]


class PolicyRuleBulkEditForm(BootstrapMixin, AddRemoveTagsForm, StatusBulkEditFormMixin, BulkEditForm):
    """PolicyRule bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=choices.ACTION_CHOICES, required=False)
    log = forms.BooleanField(required=False)
    source = DynamicModelChoiceField(queryset=models.SourceDestination.objects.all(), label="Source", required=False)
    destination = DynamicModelChoiceField(
        queryset=models.SourceDestination.objects.all(), label="Destination", required=False
    )

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class PolicyFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm):
    """Filter form to filter searches."""

    model = models.Policy
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class PolicyForm(BootstrapMixin, forms.ModelForm):
    """Policy creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = ["name", "description", "policy_rules", "status"]


class PolicyBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """Policy bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Policy.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]
