"""Tables for Firewall models."""

import django_tables2 as tables
from django_tables2.utils import A
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn

from nautobot_plugin_firewall_model import models


class IPRangeTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    start_address = tables.Column(linkify=True)
    vrf = tables.LinkColumn()
    actions = ButtonsColumn(models.IPRange, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.IPRange
        fields = (
            "pk",
            "start_address",
            "end_address",
            "vrf",
            "size",
            "description",
        )


class FQDNTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.FQDN, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.FQDN
        fields = (
            "pk",
            "name",
            "description",
        )


class AddressObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObject
        fields = ("pk", "name", "description", "ip_address", "ip_range", "prefix", "fqdn")


class AddressObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = (
            "pk",
            "name",
            "description",
            "address_objects",
        )


class AddressPolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressPolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = ("pk", "name", "description", "address_objects", "address_object_groups")


class ServiceObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObject
        fields = (
            "pk",
            "name",
            "port",
            "ip_protocol",
            "description",
        )


class ServiceObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = (
            "pk",
            "name",
            "description",
            "service_objects",
        )


class ServicePolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServicePolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = (
            "pk",
            "name",
            "description",
            "service_objects",
            "service_object_groups",
        )


class UserObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    username = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObject
        fields = (
            "pk",
            "username",
            "name",
        )


class UserObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = (
            "pk",
            "name",
            "description",
            "user_objects",
        )


class UserPolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserPolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = (
            "pk",
            "name",
            "description",
            "user_objects",
            "user_object_groups",
        )


class ZoneTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Zone, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Zone
        fields = (
            "pk",
            "name",
            "vrfs",
            "interfaces",
            "description",
        )


class SourceTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    display = tables.LinkColumn(
        "plugins:nautobot_plugin_firewall_model:source",
        text=lambda record: str(record),  # pylint: disable=W0108
        args=[A("pk")],
    )
    actions = ButtonsColumn(models.Source, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Source
        fields = (
            "pk",
            "display",
            "description",
            "address",
            "service",
            "user",
            "zone",
        )


class DestinationTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    display = tables.LinkColumn(
        "plugins:nautobot_plugin_firewall_model:destination",
        text=lambda record: str(record),  # pylint: disable=W0108
        args=[A("pk")],
    )
    actions = ButtonsColumn(models.Destination, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Destination
        fields = (
            "pk",
            "display",
            "description",
            "address",
            "service",
            "zone",
        )


class PolicyRuleTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.LinkColumn()
    actions = ButtonsColumn(models.PolicyRule, buttons=("edit", "delete"))
    source = tables.LinkColumn()
    destination = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.PolicyRule
        fields = (
            "pk",
            "name",
            "index",
            "action",
            "log",
            "source",
            "destination",
        )


class PolicyTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Policy, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Policy
        fields = (
            "pk",
            "name",
            "description",
            "policy_rules",
        )
