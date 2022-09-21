"""Set of choices to use in firewall models."""

from netutils.protocol_mapper import PROTO_NAME_TO_NUM


IP_PROTOCOL_CHOICES = tuple((i, i) for i in PROTO_NAME_TO_NUM.keys())  # pylint: disable=consider-iterating-dictionary

ACTION_CHOICES = (("allow", "allow"), ("deny", "deny"), ("drop", "drop"), ("remark", "remark"))

# TODO
# Thoughts:
# - Basic case of 1-to-1 swapping out the source or the destination address for another
# - Pooled case of 1-to-1 swapping where there is no fixed mapping (needed?
MODE_CHOICES = (("one-to-one", "one-to-one"), ("one-to-many", "one-to-many"), ("remark", "remark"))
