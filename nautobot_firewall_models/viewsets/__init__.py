"""UI Viewsets."""

from nautobot_firewall_models.viewsets.address import (
    AddressObjectGroupUIViewSet,
    AddressObjectUIViewSet,
    FQDNUIViewSet,
    IPRangeUIViewSet,
)
from nautobot_firewall_models.viewsets.capirca_policy import CapircaPolicyDeviceUIViewSet, CapircaPolicyUIViewSet
from nautobot_firewall_models.viewsets.nat_policy import NATPolicyRuleUIViewSet, NATPolicyUIViewSet
from nautobot_firewall_models.viewsets.security_policy import PolicyRuleUIViewSet, PolicyUIViewSet
from nautobot_firewall_models.viewsets.service import (
    ApplicationObjectGroupUIViewSet,
    ApplicationObjectUIViewSet,
    ServiceObjectGroupUIViewSet,
    ServiceObjectUIViewSet,
)
from nautobot_firewall_models.viewsets.user import UserObjectGroupUIViewSet, UserObjectUIViewSet
from nautobot_firewall_models.viewsets.zone import ZoneUIViewSet

__all__ = (
    "AddressObjectUIViewSet",
    "AddressObjectGroupUIViewSet",
    "ApplicationObjectUIViewSet",
    "ApplicationObjectGroupUIViewSet",
    "CapircaPolicyUIViewSet",
    "CapircaPolicyDeviceUIViewSet",
    "FQDNUIViewSet",
    "IPRangeUIViewSet",
    "NATPolicyRuleUIViewSet",
    "NATPolicyUIViewSet",
    "PolicyUIViewSet",
    "PolicyRuleUIViewSet",
    "ServiceObjectUIViewSet",
    "ServiceObjectGroupUIViewSet",
    "UserObjectUIViewSet",
    "UserObjectGroupUIViewSet",
    "ZoneUIViewSet",
)
