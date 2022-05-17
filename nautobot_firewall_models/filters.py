"""Filtering for Firewall Model Plugin."""

from nautobot.extras.filters import StatusModelFilterSetMixin, NautobotFilterSet
from nautobot.utilities.filters import TagFilter

from nautobot_firewall_models import models


class IPRangeFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for IPRange."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # fields = ["id", "start_address", "end_address", "vrf", "size", "description"]
        fields = ["id", "vrf", "size", "description"]


class FQDNFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for FQDN."""

    class Meta:
        """Meta attributes for filter."""

        model = models.FQDN

        fields = ["id", "name", "description"]


class AddressObjectFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for AddressObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObject

        fields = ["id", "name", "ip_address", "prefix", "ip_range", "fqdn", "description"]


class AddressObjectGroupFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for AddressObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressObjectGroup

        fields = ["id", "name", "address_objects", "description"]


class ServiceObjectFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for ServiceObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObject

        fields = ["id", "name", "ip_protocol", "port", "description"]


class ServiceObjectGroupFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for ServiceObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceObjectGroup

        fields = ["id", "name", "service_objects", "description"]


class UserObjectFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for UserObject."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObject
        fields = ["id", "name", "username"]


class UserObjectGroupFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for UserObjectGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserObjectGroup
        fields = ["id", "name", "user_objects", "description"]


class ZoneFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for Zone."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Zone

        fields = ["id", "name", "vrfs", "interfaces", "description"]


# TODO: Refactor to allow for better filtering, currently very limited.
class PolicyRuleFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for PolicyRule."""

    tag = TagFilter()

    class Meta:
        """Meta attributes for filter."""

        model = models.PolicyRule
        fields = ["id", "action", "log"]


class PolicyFilterSet(StatusModelFilterSetMixin, NautobotFilterSet):
    """Filter for Policy."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Policy
        fields = ["id", "name", "description", "policy_rules", "assigned_devices", "assigned_dynamic_groups"]
