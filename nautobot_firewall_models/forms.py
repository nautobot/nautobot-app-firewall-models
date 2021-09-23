"""Forms for the Firewall plugin."""

from django import forms
from nautobot.dcim.models import Interface
from nautobot.extras.forms import AddRemoveTagsForm
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


class IPRangeFilterForm(BootstrapMixin, forms.Form):
    """Filter form to filter searches."""

    model = models.IPRange
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    start_address = forms.CharField(required=False, label="Starting Address")
    end_address = forms.CharField(required=False, label="Ending Address")
    vrf = forms.ModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)


class IPRangeForm(BootstrapMixin, fields.IPRangeFieldMixin, forms.ModelForm):
    """IPRange creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = [
            "vrf",
            "description",
        ]


class IPRangeBulkEditForm(BootstrapMixin, BulkEditForm):
    """IPRange bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.IPRange.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    # start_address = forms.CharField(required=False)
    # end_address = forms.CharField(required=False)
    vrf = forms.ModelChoiceField(queryset=VRF.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
            "vrf",
        ]


class FQDNFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "ip_addresses"]


class FQDNForm(BootstrapMixin, forms.ModelForm):
    """FQDN creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["name", "description", "ip_addresses"]


class FQDNBulkEditForm(BootstrapMixin, BulkEditForm):
    """FQDN bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.FQDN.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "ip_addresses"]


class AddressObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

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

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectForm(BootstrapMixin, forms.ModelForm):
    """AddressObject creation/edit form."""

    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="IP Address")
    ip_range = DynamicModelChoiceField(queryset=models.IPRange.objects.all(), required=False, label="IP Range")
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False, label="Prefix")
    fqdn = DynamicModelChoiceField(queryset=models.FQDN.objects.all(), required=False, label="FQDN")

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = ["name", "description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """AddressObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.AddressObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "name",
            "description",
            "address_objects",
        ]


class AddressObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """AddressObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = [
            "name",
            "description",
            "address_objects",
        ]


class AddressObjectGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """AddressObjectGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class AddressPolicyObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.AddressPolicyObject
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "address_objects", "address_object_groups"]


class AddressPolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """AddressPolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = ["name", "description", "address_objects", "address_object_groups"]


class AddressPolicyObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """AddressPolicyObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.AddressPolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "address_objects", "address_object_groups"]


class ServiceObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    port = forms.IntegerField(required=False)
    ip_protocol = forms.ChoiceField(choices=choices.IP_PROTOCOL_CHOICES)

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "port", "ip_protocol"]


class ServiceObjectForm(BootstrapMixin, forms.ModelForm):
    """ServiceObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = ["name", "description", "port", "ip_protocol"]


class ServiceObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """ServiceObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "port", "ip_protocol"]


class ServiceObjectGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "service_objects"]


class ServiceObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """ServiceObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ["name", "description", "service_objects"]


class ServiceObjectGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """ServiceObjectGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ServicePolicyObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.ServicePolicyObject
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "service_objects", "service_object_groups"]


class ServicePolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """ServicePolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = ["name", "description", "service_objects", "service_object_groups"]


class ServicePolicyObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """ServicePolicyObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ServicePolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "service_objects", "service_object_groups"]


class UserObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    username = forms.CharField(required=False, label="Username")

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "username",
            "name",
        ]


class UserObjectForm(BootstrapMixin, forms.ModelForm):
    """UserObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = [
            "username",
            "name",
        ]


class UserObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """UserObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.UserObject.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "name",
        ]


class UserObjectGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "user_objects"]


class UserObjectGroupForm(BootstrapMixin, forms.ModelForm):
    """UserObjectGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ["name", "description", "user_objects"]


class UserObjectGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """UserObjectGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.UserObjectGroup.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class UserPolicyObjectFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.UserPolicyObject
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "user_objects", "user_object_groups"]


class UserPolicyObjectForm(BootstrapMixin, forms.ModelForm):
    """UserPolicyObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = ["name", "description", "user_objects", "user_object_groups"]


class UserPolicyObjectBulkEditForm(BootstrapMixin, BulkEditForm):
    """UserPolicyObject bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.UserPolicyObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "user_objects", "user_object_groups"]


class ZoneFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    vrfs = forms.ModelChoiceField(queryset=VRF.objects.all(), label="VRF")
    interfaces = forms.ModelChoiceField(queryset=Interface.objects.all(), label="Interface")

    class Meta:
        """Meta attributes."""

        model = models.Zone
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "vrfs", "interfaces"]


class ZoneForm(BootstrapMixin, forms.ModelForm):
    """Zone creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = ["name", "description", "vrfs", "interfaces"]


class ZoneBulkEditForm(BootstrapMixin, BulkEditForm):
    """Zone bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Zone.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    interfaces = DynamicModelMultipleChoiceField(queryset=Interface.objects.all(), required=False, label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


class SourceFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    display = forms.CharField(required=False, label="Display")

    class Meta:
        """Meta attributes."""

        model = models.Source
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "display",
            "description",
            "address",
            "service",
            "user",
            "zone",
        ]


class SourceForm(BootstrapMixin, forms.ModelForm):
    """Source creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Source
        fields = [
            "description",
            "address",
            "service",
            "user",
            "zone",
        ]


class SourceBulkEditForm(BootstrapMixin, BulkEditForm):
    """Source bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Source.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "user", "zone"]


class DestinationFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    display = forms.CharField(required=False, label="Display")

    class Meta:
        """Meta attributes."""

        model = models.Destination
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "display",
            "description",
            "address",
            "service",
            "zone",
        ]


class DestinationForm(BootstrapMixin, forms.ModelForm):
    """Destination creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Destination
        fields = [
            "description",
            "address",
            "service",
            "zone",
        ]


class DestinationBulkEditForm(BootstrapMixin, BulkEditForm):
    """Destination bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Destination.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "zone"]


class PolicyRuleFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="name")
    tag = TagFilterField(models.PolicyRule)

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "index", "action", "log", "source", "destination", "tags"]


class PolicyRuleForm(BootstrapMixin, forms.ModelForm):
    """PolicyRule creation/edit form."""

    name = forms.CharField(required=False, label="Name")
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = ["name", "index", "action", "log", "source", "destination", "tags"]


class PolicyRuleBulkEditForm(BootstrapMixin, AddRemoveTagsForm, BulkEditForm):
    """PolicyRule bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=choices.ACTION_CHOICES, required=False)
    log = forms.BooleanField(required=False)
    source = forms.ModelChoiceField(queryset=models.Source.objects.all(), label="Source", required=False)
    destination = forms.ModelChoiceField(queryset=models.Destination.objects.all(), label="Destination", required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class PolicyFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.Policy
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "policy_rules"]


class PolicyForm(BootstrapMixin, forms.ModelForm):
    """Policy creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = ["name", "description", "policy_rules"]


class PolicyBulkEditForm(BootstrapMixin, BulkEditForm):
    """Policy bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Policy.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]
