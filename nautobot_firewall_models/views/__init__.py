"""UI Viewsets."""

from nautobot_firewall_models.views.address import (
    AddressObjectGroupUIViewSet,
    AddressObjectUIViewSet,
    FQDNUIViewSet,
    IPRangeUIViewSet,
)
from nautobot_firewall_models.views.capirca_policy import CapircaPolicyUIViewSet
from nautobot_firewall_models.views.firewall_config import FirewallConfigUIViewSet
from nautobot_firewall_models.views.nat_policy import NATPolicyRuleUIViewSet, NATPolicyUIViewSet
from nautobot_firewall_models.views.security_policy import PolicyRuleUIViewSet, PolicyUIViewSet
from nautobot_firewall_models.views.service import (
    ApplicationObjectGroupUIViewSet,
    ApplicationObjectUIViewSet,
    ServiceObjectGroupUIViewSet,
    ServiceObjectUIViewSet,
)
from nautobot_firewall_models.views.user import UserObjectGroupUIViewSet, UserObjectUIViewSet
from nautobot_firewall_models.views.zone import ZoneUIViewSet

__all__ = (
    "AddressObjectUIViewSet",
    "AddressObjectGroupUIViewSet",
    "ApplicationObjectUIViewSet",
    "ApplicationObjectGroupUIViewSet",
    "CapircaPolicyUIViewSet",
    "FirewallConfigUIViewSet",
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
