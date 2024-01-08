"""Forms for the Firewall app."""

from django import forms
from nautobot.dcim.models import Device, Interface
from nautobot.extras.forms import (
    CustomFieldModelCSVForm,
    LocalContextFilterForm,
    LocalContextModelBulkEditForm,
    LocalContextModelForm,
    NautobotBulkEditForm,
    NautobotFilterForm,
    NautobotModelForm,
)
from nautobot.extras.models import DynamicGroup, Tag
from nautobot.ipam.models import VRF, IPAddress, Prefix
from nautobot.tenancy.forms import TenancyFilterForm, TenancyForm
from nautobot.tenancy.models import Tenant
from nautobot.apps.forms import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
    add_blank_choice,
)

from nautobot_firewall_models import choices, fields, models


class IPRangeFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class IPRangeForm(fields.IPRangeFieldMixin, LocalContextModelForm, NautobotModelForm):
    """IPRange creation/edit form."""

    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), label="VRF", required=False)

    class Meta:
        """Meta attributes."""

        model = models.IPRange
        fields = ["vrf", "description", "status", "tags"]


class IPRangeBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """IPRange bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.IPRange.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    # start_address = forms.CharField(required=False)
    # end_address = forms.CharField(required=False)
    vrf = DynamicModelChoiceField(queryset=VRF.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrf"]


class FQDNFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.FQDN
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class FQDNForm(LocalContextModelForm, NautobotModelForm):
    """FQDN creation/edit form."""

    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = ["name", "description", "ip_addresses", "status", "tags"]


class FQDNBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """FQDN bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.FQDN.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    ip_addresses = DynamicModelMultipleChoiceField(queryset=IPAddress.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "ip_addresses"]


class AddressObjectFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class AddressObjectForm(LocalContextModelForm, NautobotModelForm):
    """AddressObject creation/edit form."""

    ip_address = DynamicModelChoiceField(queryset=IPAddress.objects.all(), required=False, label="IP Address")
    ip_range = DynamicModelChoiceField(queryset=models.IPRange.objects.all(), required=False, label="IP Range")
    prefix = DynamicModelChoiceField(queryset=Prefix.objects.all(), required=False, label="Prefix")
    fqdn = DynamicModelChoiceField(queryset=models.FQDN.objects.all(), required=False, label="FQDN")

    class Meta:
        """Meta attributes."""

        model = models.AddressObject
        fields = ["name", "description", "fqdn", "ip_range", "ip_address", "prefix", "status", "tags"]


class AddressObjectBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """AddressObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.AddressObject.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "fqdn", "ip_range", "ip_address", "prefix"]


class AddressObjectGroupFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.AddressObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class AddressObjectGroupForm(LocalContextModelForm, NautobotModelForm):
    """AddressObjectGroup creation/edit form."""

    address_objects = DynamicModelMultipleChoiceField(queryset=models.AddressObject.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = ["name", "description", "address_objects", "status", "tags"]


class AddressObjectGroupBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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


class ApplicationObjectFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.ApplicationObject
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    category = DynamicModelChoiceField(
        queryset=models.ApplicationObject.objects.all(), required=False, label="Category"
    )


class ApplicationObjectForm(LocalContextModelForm, NautobotModelForm):
    """ApplicationObject creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ApplicationObject
        fields = [
            "name",
            "description",
            "category",
            "subcategory",
            "technology",
            "risk",
            "default_type",
            "default_ip_protocol",
            "status",
        ]


class ApplicationObjectBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """ApplicationObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.ApplicationObject.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)
    risk = forms.IntegerField(required=False)
    technology = forms.CharField(required=False)
    category = forms.CharField(required=False)
    subcategory = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
            "default_ip_protocol",
            "default_type",
            "technology",
            "category",
            "subcategory",
        ]


class ApplicationObjectGroupFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.ApplicationObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class ApplicationObjectGroupForm(LocalContextModelForm, NautobotModelForm):
    """ApplicationObjectGroup creation/edit form."""

    application_objects = DynamicModelMultipleChoiceField(queryset=models.ApplicationObject.objects.all())

    class Meta:
        """Meta attributes."""

        model = models.ApplicationObjectGroup
        fields = ["name", "description", "application_objects", "status", "tags"]


class ApplicationObjectGroupBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """ApplicationObjectGroup bulk edit form."""

    pk = DynamicModelMultipleChoiceField(
        queryset=models.ApplicationObjectGroup.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ServiceObjectFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class ServiceObjectForm(LocalContextModelForm, NautobotModelForm):
    """ServiceObject creation/edit form."""

    port = forms.CharField(
        help_text="Must be a single integer representation of port OR single port range without spaces (e.g. 80 or 8080-8088)",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.ServiceObject
        fields = ["name", "description", "port", "ip_protocol", "status", "tags"]


class ServiceObjectBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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


class ServiceObjectGroupFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.ServiceObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class ServiceObjectGroupForm(LocalContextModelForm, NautobotModelForm):
    """ServiceObjectGroup creation/edit form."""

    service_objects = DynamicModelMultipleChoiceField(queryset=models.ServiceObject.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ["name", "description", "service_objects", "status", "tags"]


class ServiceObjectGroupBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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


class UserObjectFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class UserObjectForm(LocalContextModelForm, NautobotModelForm):
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


class UserObjectBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """UserObject bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "name",
        ]


class UserObjectGroupFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.UserObjectGroup
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")


class UserObjectGroupForm(LocalContextModelForm, NautobotModelForm):
    """UserObjectGroup creation/edit form."""

    user_objects = DynamicModelMultipleChoiceField(queryset=models.UserObject.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ["name", "description", "user_objects", "status", "tags"]


class UserObjectGroupBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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


class ZoneFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class ZoneForm(LocalContextModelForm, NautobotModelForm):
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


class ZoneBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """Zone bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.Zone.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    vrfs = DynamicModelMultipleChoiceField(queryset=VRF.objects.all(), required=False, label="VRF")
    interfaces = DynamicModelMultipleChoiceField(queryset=Interface.objects.all(), required=False, label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


class PolicyRuleFilterForm(LocalContextFilterForm, NautobotFilterForm):
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


class PolicyRuleForm(LocalContextModelForm, NautobotModelForm):
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
        queryset=models.ServiceObject.objects.all(), label="Source Service Objects", required=False
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
    applications = DynamicModelMultipleChoiceField(
        queryset=models.ApplicationObject.objects.all(), label="Destination Application Objects", required=False
    )
    application_groups = DynamicModelMultipleChoiceField(
        queryset=models.ApplicationObjectGroup.objects.all(),
        label="Destination Application Object Groups",
        required=False,
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
            "applications",
            "application_groups",
            "action",
            "log",
            "status",
            "tags",
            "request_id",
            "description",
        )


# TODO: Refactor
class PolicyRuleBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """PolicyRule bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.PolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=add_blank_choice(choices.ACTION_CHOICES), required=False)
    log = forms.BooleanField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class PolicyFilterForm(LocalContextFilterForm, NautobotFilterForm, TenancyFilterForm):
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


class PolicyForm(LocalContextModelForm, NautobotModelForm, TenancyForm):
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


class PolicyBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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


# NATPolicy


class NATPolicyRuleFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name"]

    model = models.NATPolicyRule
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    tag = TagFilterField(models.NATPolicyRule)


class NATPolicyRuleForm(LocalContextModelForm, NautobotModelForm):
    """NATPolicyRule creation/edit form."""

    # Metadata
    name = forms.CharField(required=False, label="Name")
    tags = DynamicModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    request_id = forms.CharField(required=False, label="Optional field for request ticket identifier.")

    # Data that can not undergo a translation
    source_zone = DynamicModelChoiceField(queryset=models.Zone.objects.all(), label="Source Zone", required=False)
    destination_zone = DynamicModelChoiceField(
        queryset=models.Zone.objects.all(), label="Destination Zone", required=False
    )

    # Original source data
    original_source_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Original Source Address Objects", required=False
    )
    original_source_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(), label="Original Source Address Object Groups", required=False
    )
    original_source_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Original Source Service Objects", required=False
    )
    original_source_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(), label="Original Source Service Object Groups", required=False
    )

    # Translated source data
    translated_source_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Translated Source Address Objects", required=False
    )
    translated_source_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(),
        label="Translated Source Address Object Groups",
        required=False,
    )
    translated_source_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Translated Source Service Objects", required=False
    )
    translated_source_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(),
        label="Translated Source Service Object Groups",
        required=False,
    )

    # Original destination data
    original_destination_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Original Destination Address Objects", required=False
    )
    original_destination_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(),
        label="Original Destination Address Object Groups",
        required=False,
    )
    original_destination_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Original Destination Service Objects", required=False
    )
    original_destination_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(),
        label="Original Destination Service Object Groups",
        required=False,
    )

    # Translated destination data
    translated_destination_addresses = DynamicModelMultipleChoiceField(
        queryset=models.AddressObject.objects.all(), label="Translated Destination Address Objects", required=False
    )
    translated_destination_address_groups = DynamicModelMultipleChoiceField(
        queryset=models.AddressObjectGroup.objects.all(),
        label="Translated Destination Address Object Groups",
        required=False,
    )
    translated_destination_services = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObject.objects.all(), label="Translated Destination Service Objects", required=False
    )
    translated_destination_service_groups = DynamicModelMultipleChoiceField(
        queryset=models.ServiceObjectGroup.objects.all(),
        label="Translated Destination Service Object Groups",
        required=False,
    )

    class Meta:
        """Meta attributes."""

        model = models.NATPolicyRule
        fields = (
            # pylint: disable=duplicate-code
            "name",
            "source_zone",
            "destination_zone",
            "original_source_addresses",
            "original_source_address_groups",
            "original_source_services",
            "original_source_service_groups",
            "translated_source_addresses",
            "translated_source_address_groups",
            "translated_source_services",
            "translated_source_service_groups",
            "original_destination_addresses",
            "original_destination_address_groups",
            "original_destination_services",
            "original_destination_service_groups",
            "translated_destination_addresses",
            "translated_destination_address_groups",
            "translated_destination_services",
            "translated_destination_service_groups",
            "remark",
            "log",
            "status",
            "tags",
            "request_id",
            "description",
        )


# TODO: Refactor
class NATPolicyRuleBulkEditForm(PolicyRuleBulkEditForm):
    """NATPolicyRule bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.NATPolicyRule.objects.all(), widget=forms.MultipleHiddenInput)
    log = forms.BooleanField(required=False)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "tags"]


class NATPolicyFilterForm(NautobotFilterForm, TenancyFilterForm):
    """Filter form to filter searches."""

    field_order = ["q", "name", "assigned_devices", "assigned_dynamic_groups"]

    model = models.NATPolicy
    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    assigned_devices = DynamicModelChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelChoiceField(queryset=DynamicGroup.objects.all(), required=False)


class NATPolicyForm(LocalContextModelForm, NautobotModelForm, TenancyForm):
    """NATPolicy creation/edit form."""

    assigned_devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelMultipleChoiceField(queryset=DynamicGroup.objects.all(), required=False)
    nat_policy_rules = DynamicModelMultipleChoiceField(queryset=models.NATPolicyRule.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        model = models.NATPolicy
        fields = [
            "name",
            "description",
            "nat_policy_rules",
            "status",
            "assigned_devices",
            "assigned_dynamic_groups",
            "tenant_group",
            "tenant",
            "tags",
        ]


class NATPolicyBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
    """NATPolicy bulk edit form."""

    pk = DynamicModelMultipleChoiceField(queryset=models.NATPolicy.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    assigned_devices = DynamicModelMultipleChoiceField(queryset=Device.objects.all(), required=False)
    assigned_dynamic_groups = DynamicModelMultipleChoiceField(queryset=DynamicGroup.objects.all(), required=False)
    policy_rules = DynamicModelMultipleChoiceField(queryset=models.NATPolicyRule.objects.all(), required=False)
    tenant = DynamicModelChoiceField(queryset=Tenant.objects.all(), required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


# CapircaPolicy


class CapircaPolicyForm(LocalContextModelForm, NautobotModelForm):
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


class CapircaPolicyFilterForm(LocalContextFilterForm, NautobotFilterForm):
    """Form for CapircaPolicy instances."""

    model = models.CapircaPolicy

    q = forms.CharField(required=False, label="Search")


class CapircaPolicyBulkEditForm(LocalContextModelBulkEditForm, NautobotBulkEditForm):
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
