"""Load models."""

from .address import (
    FQDN,
    AddressObject,
    AddressObjectGroup,
    IPRange,
)
from .capirca_policy import (
    CapircaPolicy,
)
from .nat_policy import (
    NATPolicy,
    NATPolicyDeviceM2M,
    NATPolicyDynamicGroupM2M,
    NATPolicyRule,
)
from .security_policy import (
    Policy,
    PolicyDeviceM2M,
    PolicyDynamicGroupM2M,
    PolicyRule,
)
from .service import (
    ApplicationObject,
    ApplicationObjectGroup,
    ServiceObject,
    ServiceObjectGroup,
)
from .user import UserObject, UserObjectGroup
from .zone import Zone

__all__ = (
    "AddressObject",
    "AddressObjectGroup",
    "ApplicationObject",
    "ApplicationObjectGroup",
    "CapircaPolicy",
    "FQDN",
    "IPRange",
    "NATPolicy",
    "NATPolicyDeviceM2M",
    "NATPolicyDynamicGroupM2M",
    "NATPolicyRule",
    "Policy",
    "PolicyDeviceM2M",
    "PolicyDynamicGroupM2M",
    "PolicyRule",
    "ServiceObject",
    "ServiceObjectGroup",
    "UserObject",
    "UserObjectGroup",
    "Zone",
)
