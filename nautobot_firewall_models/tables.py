"""Tables for Firewall models."""

import django_tables2 as tables
from django_tables2.utils import A
from nautobot.utilities.tables import BaseTable, ButtonsColumn, ToggleColumn

from nautobot_firewall_models import models


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
        fields = ("pk", "start_address", "end_address", "vrf", "size", "description", "status")


class FQDNTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.FQDN, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.FQDN
        fields = ("pk", "name", "description", "ip_addresses", "status")


class AddressObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObject
        fields = ("pk", "name", "description", "ip_address", "ip_range", "prefix", "fqdn", "status")


class AddressObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressObjectGroup
        fields = ("pk", "name", "description", "address_objects", "status")


class AddressPolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.AddressPolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.AddressPolicyObject
        fields = ("pk", "name", "description", "address_objects", "address_object_groups", "status")


class ServiceObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObject
        fields = ("pk", "name", "port", "ip_protocol", "description", "status")


class ServiceObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServiceObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServiceObjectGroup
        fields = ("pk", "name", "description", "service_objects", "status")


class ServicePolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.ServicePolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.ServicePolicyObject
        fields = ("pk", "name", "description", "service_objects", "service_object_groups", "status")


class UserObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    username = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObject
        fields = ("pk", "username", "name", "status")


class UserObjectGroupTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserObjectGroup, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserObjectGroup
        fields = ("pk", "name", "description", "user_objects", "status")


class UserPolicyObjectTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.UserPolicyObject, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.UserPolicyObject
        fields = ("pk", "name", "description", "user_objects", "user_object_groups", "status")


class ZoneTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Zone, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Zone
        fields = ("pk", "name", "vrfs", "interfaces", "description", "status")


class SourceDestinationTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    display = tables.LinkColumn(
        "plugins:nautobot_firewall_models:source",
        text=lambda record: str(record),  # pylint: disable=W0108
        args=[A("pk")],
    )
    actions = ButtonsColumn(models.SourceDestination, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.SourceDestination
        fields = ("pk", "display", "description", "address", "service", "user", "zone", "status")


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
        fields = ("pk", "name", "index", "action", "log", "source", "destination", "status")


class PolicyTable(BaseTable):
    # pylint: disable=R0903
    """Table for list view."""

    pk = ToggleColumn()
    name = tables.Column(linkify=True)
    actions = ButtonsColumn(models.Policy, buttons=("edit", "delete"))

    class Meta(BaseTable.Meta):
        """Meta attributes."""

        model = models.Policy
        fields = ("pk", "name", "description", "policy_rules", "status")
