"""Tables for Firewall models."""

import django_tables2 as tables
from nautobot.extras.tables import StatusTableMixin
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn

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
        )


class PolicyTable(StatusTableMixin, BaseTable):
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Policy, buttons=("edit", "delete"))
    assigned_devices = tables.ManyToManyColumn(linkify_item=True)
    assigned_dynamic_groups = tables.ManyToManyColumn(linkify_item=True)

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Policy
        fields = ("pk", "name", "description", "policy_rules", "assigned_devices", "assigned_dynamic_groups", "status")
