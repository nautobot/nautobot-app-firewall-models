"""Set of choices to use in firewall models."""

from nautobot.core.choices import ChoiceSet
from netutils.protocol_mapper import PROTO_NAME_TO_NUM

IP_PROTOCOL_CHOICES = tuple((i, i) for i in PROTO_NAME_TO_NUM.keys())  # pylint: disable=consider-iterating-dictionary

ACTION_CHOICES = (("allow", "allow"), ("deny", "deny"), ("drop", "drop"), ("remark", "remark"))


class FirewallConfigChoice(ChoiceSet):
    """Choiceset used by FirewallConfig."""

    TYPE_CAPIRCA = "capirca"
    TYPE_AERLEON = "aerleon"
    TYPE_CUSTOM = "custom_firewall_config"

    CHOICES = (
        (TYPE_CAPIRCA, "CAPIRCA"),
        (TYPE_AERLEON, "AERLEON"),
        (TYPE_CUSTOM, "CUSTOM_FIREWALL_CONFIG"),
    )
