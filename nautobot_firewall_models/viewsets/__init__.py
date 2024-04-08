"""UI Viewsets."""
from nautobot_firewall_models.viewsets.address import (
    AddressObjectUIViewSet,
    AddressObjectGroupUIViewSet,
    FQDNUIViewSet,
    IPRangeUIViewSet,
)
from nautobot_firewall_models.viewsets.aerleon_policy import AerleonPolicyUIViewSet, AerleonPolicyDeviceUIViewSet
from nautobot_firewall_models.viewsets.nat_policy import NATPolicyRuleUIViewSet, NATPolicyUIViewSet
from nautobot_firewall_models.viewsets.security_policy import PolicyUIViewSet, PolicyRuleUIViewSet
from nautobot_firewall_models.viewsets.service import (
    ApplicationObjectUIViewSet,
    ApplicationObjectGroupUIViewSet,
    ServiceObjectUIViewSet,
    ServiceObjectGroupUIViewSet,
)
from nautobot_firewall_models.viewsets.user import UserObjectUIViewSet, UserObjectGroupUIViewSet
from nautobot_firewall_models.viewsets.zone import ZoneUIViewSet


__all__ = (
    "AddressObjectUIViewSet",
    "AddressObjectGroupUIViewSet",
    "AerleonPolicyUIViewSet",
    "AerleonPolicyDeviceUIViewSet",
    "ApplicationObjectUIViewSet",
    "ApplicationObjectGroupUIViewSet",
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
