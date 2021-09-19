"""Forms for the Firewall plugin."""

from django import forms
from nautobot.dcim.models import Interface
from nautobot.ipam.models import VRF
from nautobot.utilities.forms import BootstrapMixin, BulkEditForm

from nautobot_plugin_firewall_model import models, fields, choices


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
        fields = [
            "q",
            "name",
            "description",
        ]


class FQDNForm(BootstrapMixin, forms.ModelForm):
    """FQDN creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.FQDN
        fields = [
            "name",
            "description",
        ]


class FQDNBulkEditForm(BootstrapMixin, BulkEditForm):
    """FQDN bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.FQDN.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class ProtocolFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    port = forms.IntegerField(required=False)

    class Meta:
        """Meta attributes."""

        model = models.Protocol
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "port", "tcp_udp"]


class ProtocolForm(BootstrapMixin, forms.ModelForm):
    """Protocol creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Protocol
        fields = ["name", "description", "port", "tcp_udp"]


class ProtocolBulkEditForm(BootstrapMixin, BulkEditForm):
    """Protocol bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Protocol.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "port", "tcp_udp"]


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

    # class Meta:
    #     """Meta attributes."""

    #     model = models.IPRange
    #     # Define the fields above for ordering and widget purposes
    #     fields = [
    #         "q",
    #         "start_address",
    #         "end_address",
    #         "vrf",
    #         "description",
    #     ]


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
    vrfs = forms.ModelMultipleChoiceField(queryset=VRF.objects.all(), label="VRF")
    interfaces = forms.ModelMultipleChoiceField(queryset=Interface.objects.all(), label="Interface")

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "vrfs", "interfaces"]


class AddressGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")
    ip_addresses = forms.ModelChoiceField(queryset=VRF.objects.all(), label="IP Address")
    ip_ranges = forms.ModelChoiceField(queryset=Interface.objects.all(), label="IP Range")
    prefixes = forms.ModelChoiceField(queryset=Interface.objects.all(), label="Prefix")

    class Meta:
        """Meta attributes."""

        model = models.AddressGroup
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "name",
            "description",
            "ip_addresses",
            "ip_ranges",
            "prefixes",
        ]


class AddressGroupForm(BootstrapMixin, forms.ModelForm):
    """AddressGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.AddressGroup
        fields = [
            "name",
            "description",
            "ip_addresses",
            "ip_ranges",
            "prefixes",
        ]


class AddressGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """AddressGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.AddressGroup.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)
    ip_addresses = forms.ModelMultipleChoiceField(queryset=VRF.objects.all(), label="IP Address")
    ip_ranges = forms.ModelMultipleChoiceField(queryset=Interface.objects.all(), label="IP Range")
    prefixes = forms.ModelMultipleChoiceField(queryset=Interface.objects.all(), label="Prefix")

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
            "ip_addresses",
            "ip_ranges",
            "prefixes",
        ]


class ServiceGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "protocols"]


class ServiceGroupForm(BootstrapMixin, forms.ModelForm):
    """ServiceGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.ServiceGroup
        fields = ["name", "description", "protocols"]


class ServiceGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """ServiceGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ServiceGroup.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class UserFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    username = forms.CharField(required=False, label="Username")

    class Meta:
        """Meta attributes."""

        model = models.User
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "username",
            "name",
        ]


class UserForm(BootstrapMixin, forms.ModelForm):
    """User creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.User
        fields = [
            "username",
            "name",
        ]


class UserBulkEditForm(BootstrapMixin, BulkEditForm):
    """User bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.User.objects.all(), widget=forms.MultipleHiddenInput)
    name = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "name",
        ]


class UserGroupFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    name = forms.CharField(required=False, label="Name")

    class Meta:
        """Meta attributes."""

        model = models.UserGroup
        # Define the fields above for ordering and widget purposes
        fields = ["q", "name", "description", "users"]


class UserGroupForm(BootstrapMixin, forms.ModelForm):
    """UserGroup creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.UserGroup
        fields = ["name", "description", "users"]


class UserGroupBulkEditForm(BootstrapMixin, BulkEditForm):
    """UserGroup bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.UserGroup.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]


class SourceDestinationFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    display = forms.CharField(required=False, label="Display")

    class Meta:
        """Meta attributes."""

        model = models.SourceDestination
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "display",
            "description",
            # "address",
            # "service",
            # "user",
            "zone",
        ]


class SourceDestinationForm(BootstrapMixin, forms.ModelForm):
    """SourceDestination creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.SourceDestination
        fields = [
            "description",
            # "address",
            # "service",
            # "user",
            "zone",
        ]


class SourceDestinationBulkEditForm(BootstrapMixin, BulkEditForm):
    """SourceDestination bulk edit form."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.SourceDestination.objects.all(), widget=forms.MultipleHiddenInput
    )
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = ["description", "user", "zone"]


class TermFilterForm(BootstrapMixin, forms.ModelForm):
    """Filter form to filter searches."""

    q = forms.CharField(
        required=False,
        label="Search",
        help_text="Search within Name or Description.",
    )
    display = forms.CharField(required=False, label="Display")

    class Meta:
        """Meta attributes."""

        model = models.Term
        # Define the fields above for ordering and widget purposes
        fields = [
            "q",
            "display",
            "index",
            "action",
            "log",
            "source",
            "destination",
        ]


class TermForm(BootstrapMixin, forms.ModelForm):
    """Term creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Term
        fields = [
            "index",
            "action",
            "log",
            "source",
            "destination",
        ]


class TermBulkEditForm(BootstrapMixin, BulkEditForm):
    """Term bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Term.objects.all(), widget=forms.MultipleHiddenInput)
    action = forms.ChoiceField(choices=choices.ACTION_CHOICES)
    log = forms.BooleanField()
    source = forms.ModelChoiceField(queryset=models.SourceDestination.objects.all(), label="Source")
    destination = forms.ModelChoiceField(queryset=models.SourceDestination.objects.all(), label="Destination")


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
        fields = ["q", "name", "description", "terms"]


class PolicyForm(BootstrapMixin, forms.ModelForm):
    """Policy creation/edit form."""

    class Meta:
        """Meta attributes."""

        model = models.Policy
        fields = ["name", "description", "terms"]


class PolicyBulkEditForm(BootstrapMixin, BulkEditForm):
    """Policy bulk edit form."""

    pk = forms.ModelMultipleChoiceField(queryset=models.Policy.objects.all(), widget=forms.MultipleHiddenInput)
    description = forms.CharField(required=False)

    class Meta:
        """Meta attributes."""

        nullable_fields = [
            "description",
        ]
