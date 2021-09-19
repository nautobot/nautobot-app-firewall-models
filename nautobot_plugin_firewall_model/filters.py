"""Filtering for VIP Tracker."""

from nautobot.extras.filters import CreatedUpdatedFilterSet
from nautobot.utilities.filters import BaseFilterSet, TagFilter

from nautobot_plugin_firewall_model import models


class IPRangeFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for IPRange."""

    class Meta:
        """Meta attributes for filter."""

        model = models.IPRange

        # fields = ["id", "start_address", "end_address", "vrf", "size", "description"]
        fields = ["id", "vrf", "size", "description"]


class ZoneFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for Zone."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Zone

        fields = ["id", "name", "vrfs", "interfaces", "description"]


class AddressGroupFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for AddressGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.AddressGroup

        fields = ["id", "name", "ip_addresses", "prefixes", "ip_ranges", "description"]


class ProtocolFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for Protocol."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Protocol

        fields = ["id", "name", "slug", "tcp_udp", "port", "description"]


class ServiceGroupFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for ServiceGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.ServiceGroup

        fields = ["id", "name", "protocols", "description"]


class FQDNFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for FQDN."""

    class Meta:
        """Meta attributes for filter."""

        model = models.FQDN

        fields = ["id", "name", "description"]


class UserFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for User."""

    class Meta:
        """Meta attributes for filter."""

        model = models.User
        fields = ["id", "name", "username"]


class UserGroupFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for UserGroup."""

    class Meta:
        """Meta attributes for filter."""

        model = models.UserGroup
        fields = ["id", "name", "users", "description"]


class SourceDestinationFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for SourceDestination."""

    class Meta:
        """Meta attributes for filter."""

        model = models.SourceDestination
        fields = [
            "id",
            # "address",
            # "user",
            # "service",
            "zone",
            "description",
        ]


class TermFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for Term."""

    tag = TagFilter()

    class Meta:
        """Meta attributes for filter."""

        model = models.Term
        fields = ["id", "index", "source", "destination", "action", "log"]


class PolicyFilter(BaseFilterSet, CreatedUpdatedFilterSet):
    """Filter for Term."""

    class Meta:
        """Meta attributes for filter."""

        model = models.Policy
        fields = ["id", "name", "description", "terms"]
