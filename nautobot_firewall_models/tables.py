"""Table Views for Firewall Models."""

import django_tables2 as tables
from nautobot.apps.tables import BaseTable, ButtonsColumn, ToggleColumn
from nautobot.extras.tables import StatusTableMixin

from nautobot_firewall_models import models


class IPRangeTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    start_address = tables.Column(linkify=True)
    vrf = tables.LinkColumn()
    actions = ButtonsColumn(models.IPRange, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.IPRange
        fields = ("pk", "start_address", "end_address", "vrf", "size", "description", "status")


class FQDNTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.FQDN, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.FQDN
        fields = ("pk", "name", "description", "ip_addresses", "status")


class AddressObjectTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObject
        fields = ("pk", "name", "description", "ip_address", "ip_range", "prefix", "fqdn", "status")


class AddressObjectGroupTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = ("pk", "name", "description", "address_objects", "status")


class ApplicationObjectTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ApplicationObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ApplicationObject
        fields = ("pk", "name", "description", "category", "subcategory", "technology", "risk", "default_type")


class ApplicationObjectGroupTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    application_objects = tables.ManyToManyColumn(linkify_item=True)
    actions = ButtonsColumn(models.ApplicationObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ApplicationObjectGroup
        fields = ("pk", "name", "description", "application_objects")


class ServiceObjectTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObject
        fields = ("pk", "name", "port", "ip_protocol", "description", "status")


class ServiceObjectGroupTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ("pk", "name", "description", "service_objects", "status")


class UserObjectTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    username = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObject
        fields = ("pk", "username", "name", "status")


class UserObjectGroupTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ("pk", "name", "description", "user_objects", "status")


class ZoneTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Zone, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Zone
        fields = ("pk", "name", "vrfs", "interfaces", "description", "status")


# TODO: refactor
class PolicyRuleTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.PolicyRule, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.PolicyRule
        fields = (
            # pylint: disable=duplicate-code
            "pk",
            "name",
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
            "description",
            "request_id",
            "log",
            "status",
        )
        default_columns = (
            "pk",
            "name",
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
        )


class PolicyTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Policy, buttons=("edit", "delete"))
    assigned_devices = tables.ManyToManyColumn(linkify_item=True)
    assigned_virtual_machines = tables.ManyToManyColumn(linkify_item=True)
    assigned_dynamic_groups = tables.ManyToManyColumn(linkify_item=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Policy
        fields = (
            "pk",
            "name",
            "description",
            "policy_rules",
            "assigned_devices",
            "assigned_virtual_machines",
            "assigned_dynamic_groups",
            "status",
        )


# TODO: refactor
class NATPolicyRuleTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.NATPolicyRule, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.NATPolicyRule
        fields = (
            # pylint: disable=duplicate-code
            "pk",
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
            "request_id",
            "description",
            "log",
            "status",
        )
        default_columns = (
            # pylint: disable=duplicate-code
            "pk",
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
        )


class NATPolicyTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    nat_policy_rules = tables.ManyToManyColumn(verbose_name="NAT policy rules", linkify_item=True)
    actions = ButtonsColumn(models.NATPolicy, buttons=("edit", "delete"))
    assigned_devices = tables.ManyToManyColumn(linkify_item=True)
    assigned_virtual_machines = tables.ManyToManyColumn(linkify_item=True)
    assigned_dynamic_groups = tables.ManyToManyColumn(linkify_item=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.NATPolicy
        fields = (
            "pk",
            "name",
            "description",
            "nat_policy_rules",
            "assigned_devices",
            "assigned_virtual_machines",
            "assigned_dynamic_groups",
            "status",
        )


class AerleonPolicyTable(BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    device = tables.TemplateColumn(
        template_code="""<a href="{% url 'plugins:nautobot_firewall_models:aerleonpolicy' pk=record.pk %}">{{ record.device }}</a> """
    )

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AerleonPolicy
        fields = ("pk", "device")
