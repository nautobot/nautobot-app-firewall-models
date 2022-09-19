"""Forms for the Firewall plugin."""

from django import forms
from nautobot.dcim.models import Interface, Device
from nautobot.extras.forms import (
    TagsBulkEditFormMixin,
    StatusModelFilterFormMixin,
    StatusModelBulkEditFormMixin,
    CustomFieldModelFilterFormMixin,
    CustomFieldModelBulkEditFormMixin,
    CustomFieldModelCSVForm,
    CustomFieldModelFormMixin,
    RelationshipModelFormMixin,
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


class IPRangeFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "start_address", "end_address", "vrf"]

    model = models.IPRange
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    start_address = forms.CharField(required=False, label="Starting Address")
    end_address = forms.CharField(required=False, label="Ending Address")
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)


class IPRangeForm(BootstrapMixin, fields.IPRangeFieldMixin, RelationshipModelFormMixin, forms.ModelForm):
    """IPRange creation/edit form."""

    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["vrf", "description", "status", "tags"]


class IPRangeBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """IPRange bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.IPRange.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    # start_address = forms.CharField(required=False)
    # end_address = forms.CharField(required=False)
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrf"]


class FQDNFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.FQDN
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class FQDNForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """FQDN creation/edit form."""

    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["name", "description", "ip_addresses", "status", "tags"]


class FQDNBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """FQDN bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.FQDN.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "ip_addresses"]


class AddressObjectFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

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


class AddressObjectForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """AddressObject creation/edit form."""

    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="IP Address")
    ip_range = DynamicModelChoiceField(queryset=models.IPRange.objects.all(), required=False, label="IP Range")
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False, label="Prefix")
    fqdn = DynamicModelChoiceField(queryset=models.FQDN.objects.all(), required=False, label="FQDN")

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = ["name", "description", "fqdn", "ip_range", "ip_address", "prefix", "status", "tags"]


class AddressObjectBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """AddressObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.AddressObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectGroupFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.AddressObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class AddressObjectGroupForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """AddressObjectGroup creation/edit form."""

    address_objects = DynamicModelMultipleChoiceField(queryset=models.AddressObject.objects.all())

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = ["name", "description", "address_objects", "status", "tags"]


class AddressObjectGroupBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
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


class ServiceObjectFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.ServiceObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    port = forms.IntegerField(required=False)
    ip_protocol = forms.ChoiceField(choices=add_blank_choice(choices.IP_PROTOCOL_CHOICES), required=False)


class ServiceObjectForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """ServiceObject creation/edit form."""

    port = forms.CharField(
        help_text="Must be a single integer representation of port OR single port range without spaces (e.g. 80 or 8080-8088)",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = ["name", "description", "port", "ip_protocol", "status", "tags"]


class ServiceObjectBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """ServiceObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    port = forms.CharField(
        help_text="Must be a single integer representation of port OR single port range without spaces (e.g. 80 or 8080-8088)",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "port"]


class ServiceObjectGroupFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.ServiceObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class ServiceObjectGroupForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """ServiceObjectGroup creation/edit form."""

    service_objects = DynamicModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ["name", "description", "service_objects", "status", "tags"]


class ServiceObjectGroupBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
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


class UserObjectFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "username", "name"]

    model = models.UserObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    username = forms.CharField(required=False, label="Username")


class UserObjectForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """UserObject creation/edit form."""

    username = forms.CharField(label="Username")
    name = forms.CharField(
        label="Name",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.UserObject
        fields = ["username", "name", "status", "tags"]


class UserObjectBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """UserObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "name",
        ]


class UserObjectGroupFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.UserObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class UserObjectGroupForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """UserObjectGroup creation/edit form."""

    user_objects = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ["name", "description", "user_objects", "status", "tags"]


class UserObjectGroupBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
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


class ZoneFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.Zone
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    vrfs = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF")
    interfaces = DynamicModelChoiceField(queryset=Interface.objects.all(), label="Interface")


class ZoneForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm):
    """Zone creation/edit form."""

    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    device = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(), required=False, label="Interface", query_params={"device_id": "$device"}
    )

    class Meta:
        """Meta attributes."""

        model = models.Zone
        fields = ["name", "description", "vrfs", "device", "interfaces", "status", "tags"]


class ZoneBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """Zone bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Zone.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    interfaces = DynamicModelMultipleChoiceField(queryset=Interface.objects.all(), required=False, label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


class PolicyRuleFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.PolicyRule
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    tag = TagFilterField(models.PolicyRule)


class PolicyRuleForm(BootstrapMixin, CustomFieldModelFormMixin, RelationshipModelFormMixin):
    """PolicyRule creation/edit form."""

    name = forms.CharField(required=False, label="Name")
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    source_users = DynamicModelMultipleChoiceField(
        queryset=models.UserObject.objects.all(), label="Source User Objects", required=False
    )
    source_user_groups = DynamicModelMultipleChoiceField(
        queryset=models.UserObjectGroup.objects.all(), label="Source User Object Groups", required=False
    )
    source_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Source Address Objects", required=False
    )
    source_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), label="Source Address Object Groups", required=False
    )
    source_zone = DynamicModelChoiceField(queryset=models.Zone.objects.all(), label="Source Zone", required=False)
    source_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Souce Service Objects", required=False
    )
    source_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), label="Source Service Object Groups", required=False
    )
    destination_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Destination Address Objects", required=False
    )
    destination_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), label="Destination Address Object Groups", required=False
    )
    destination_zone = DynamicModelChoiceField(
        queryset=models.Zone.objects.all(), label="Destination Zone", required=False
    )
    destination_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Destination Service Objects", required=False
    )
    destination_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), label="Destination Service Object Groups", required=False
    )
    request_id = forms.CharField(required=False, label="Optional field for request ticket identifier.")

    class Meta:
        """Meta attributes."""

        model = models.PolicyRule
        fields = (
            # pylint: disable=duplicate-code
            "name",
            "index",
            "source_users",
            "source_user_groups",
            "source_addresses",
            "source_address_groups",
            "source_zone",
            "source_services",
            "source_service_groups",
            "destination_addresses",
            "destination_address_groups",
            "destination_zone",
            "destination_services",
            "destination_service_groups",
            "action",
            "log",
            "status",
            "tags",
            "request_id",
            "description",
        )


# TODO: Refactor
class PolicyRuleBulkEditForm(BootstrapMixin, TagsBulkEditFormMixin, StatusModelBulkEditFormMixin, BulkEditForm):
    """PolicyRule bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=add_blank_choice(choices.ACTION_CHOICES), required=False)
    log = forms.BooleanField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class PolicyFilterForm(BootstrapMixin, StatusModelFilterFormMixin, CustomFieldModelFilterFormMixin, TenancyFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name", "assigned_devices", "assigned_dynamic_groups"]

    model = models.Policy
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    assigned_devices = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelChoiceField(queryset=DynamicGroup.objects.all(), required=False)


class PolicyForm(BootstrapMixin, RelationshipModelFormMixin, forms.ModelForm, TenancyForm):
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


class PolicyBulkEditForm(BootstrapMixin, StatusModelBulkEditFormMixin, BulkEditForm):
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


# CapircaPolicy


class CapircaPolicyForm(BootstrapMixin, CustomFieldModelFormMixin, RelationshipModelFormMixin):
    """Filter Form for CapircaPolicy instances."""

    device = DynamicModelChoiceField(queryset=Device.objects.all())

    class Meta:
        """Boilerplate form Meta data for compliance rule."""

        model = models.CapircaPolicy
        fields = (
            "device",
            "pol",
            "net",
            "svc",
            "cfg",
        )


class CapircaPolicyFilterForm(BootstrapMixin, CustomFieldModelFilterFormMixin):
    """Form for CapircaPolicy instances."""

    model = models.CapircaPolicy

    q = forms.CharField(required=False, label="Search")


class CapircaPolicyBulkEditForm(BootstrapMixin, TagsBulkEditFormMixin, CustomFieldModelBulkEditFormMixin):
    """BulkEdit form for CapircaPolicy instances."""

    pk = forms.ModelMultipleChoiceField(queryset=models.CapircaPolicy.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Boilerplate form Meta data for CapircaPolicy."""

        nullable_fields = []


class CapircaPolicyCSVForm(CustomFieldModelCSVForm):
    """CSV Form for CapircaPolicy instances."""

    class Meta:
        """Boilerplate form Meta data for CapircaPolicy."""

        model = models.CapircaPolicy
        fields = models.CapircaPolicy.csv_headers
