"""Forms for the Firewall plugin."""

from django import forms
from nautobot.dcim.models import Interface, Device
from nautobot.extras.forms import (
    AddRemoveTagsForm,
    StatusFilterFormMixin,
    StatusBulkEditFormMixin,
    CustomFieldFilterForm,
)
from nautobot.extras.models import Tag, DynamicGroup
from nautobot.ipam.models import VRF, Prefix, IPAddress
from nautobot.tenancy.forms import TenancyFilterForm, TenancyForm
from nautobot.tenancy.models import Tenant
from nautobot.utilities.forms import (
    BootstrapMixin,
    BulkEditForm,
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    add_blank_choice,
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

    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["vrf", "description", "status", "tags"]


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

    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["name", "description", "ip_addresses", "status", "tags"]


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
        fields = ["name", "description", "fqdn", "ip_range", "ip_address", "prefix", "status", "tags"]


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
        fields = ["name", "description", "address_objects", "status", "tags"]


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
    ip_protocol = forms.ChoiceField(choices=choices.IP_PROTOCOL_CHOICES, required=False)


class ServiceObjectForm(BootstrapMixin, forms.ModelForm):
    """ServiceObject creation/edit form."""

    port = forms.CharField(
        help_text="Must be a single integer representation of port OR single port range without spaces (i.e. 80 or 8080-8088)",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = ["name", "description", "port", "ip_protocol", "status", "tags"]


class ServiceObjectBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """ServiceObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    port = forms.CharField(
        help_text="Must be a single integer representation of port OR single port range without spaces (i.e. 80 or 8080-8088)",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "port"]


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
        fields = ["name", "description", "service_objects", "status", "tags"]


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

    username = forms.CharField(
        help_text="Signifies the username in identify provider (i.e. john.smith)", label="Username"
    )
    name = forms.CharField(
        help_text="Signifies the name of the user, commonly first & last name (i.e. John Smith)",
        label="Name",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = ["username", "name", "status", "tags"]


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

    user_objects = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all())

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ["name", "description", "user_objects", "status", "tags"]


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

    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = ["name", "description", "vrfs", "interfaces", "status", "tags"]


class ZoneBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """Zone bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Zone.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    interfaces = DynamicModelMultipleChoiceField(queryset=Interface.objects.all(), required=False, label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


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
    source_user = DynamicModelMultipleChoiceField(
        queryset=models.UserObject.objects.all(), label="Source User Objects", required=False
    )
    source_user_group = DynamicModelMultipleChoiceField(
        queryset=models.UserObjectGroup.objects.all(), label="Source User Object Groups", required=False
    )
    source_address = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Source Address Objects", required=False
    )
    source_address_group = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), label="Source Address Object Groups", required=False
    )
    source_zone = DynamicModelChoiceField(queryset=models.Zone.objects.all(), label="Source Zone", required=False)
    destination_address = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Destination Address Objects", required=False
    )
    destination_address_group = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), label="Destination Address Object Groups", required=False
    )
    destination_zone = DynamicModelChoiceField(
        queryset=models.Zone.objects.all(), label="Destination Zone", required=False
    )
    service = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Service Objects", required=False
    )
    service_group = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), label="Service Object Groups", required=False
    )
    request_id = forms.CharField(required=False, label="Optional field for request ticket identifier.")

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = [
            # pylint: disable=R0801
            "name",
            "source_user",
            "source_user_group",
            "source_address",
            "source_address_group",
            "source_zone",
            "destination_address",
            "destination_address_group",
            "destination_zone",
            "service",
            "service_group",
            "action",
            "log",
            "status",
            "tags",
            "request_id",
        ]


# TODO: Refactor
class PolicyRuleBulkEditForm(BootstrapMixin, AddRemoveTagsForm, StatusBulkEditFormMixin, BulkEditForm):
    """PolicyRule bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=add_blank_choice(choices.ACTION_CHOICES), required=False)
    log = forms.BooleanField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class PolicyFilterForm(BootstrapMixin, StatusFilterFormMixin, CustomFieldFilterForm, TenancyFilterForm):
    """Filter form to filter searches."""

    model = models.Policy
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    assigned_devices = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)


class PolicyForm(BootstrapMixin, forms.ModelForm, TenancyForm):
    """Policy creation/edit form."""

    assigned_devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelMultipleChoiceField(queryset=DynamicGroup.objects.all(), required=False)
    policy_rules = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = [
            "name",
            "description",
            "policy_rules",
            "status",
            "assigned_devices",
            "assigned_dynamic_groups",
            "tenant_group",
            "tenant",
            "tags",
        ]


class PolicyBulkEditForm(BootstrapMixin, StatusBulkEditFormMixin, BulkEditForm):
    """Policy bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Policy.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    assigned_devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelMultipleChoiceField(queryset=DynamicGroup.objects.all(), required=False)
    policy_rules = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]
