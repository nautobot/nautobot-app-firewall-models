"""Set of choices to use in firewall models."""

from django.db.models import Q

TCP_UDP_CHOICES = (
    (
        "TCP",
        "tcp",
    ),
    ("UDP", "udp"),
)

ADDRESS_ASSIGNMENT_MODELS = Q(
    Q(app_label="ipam", model="ipaddress")
    | Q(app_label="ipam", model="prefix")
    | Q(app_label="nautobot_plugin_firewall_model", model="iprange")
)

ACTION_CHOICES = (("Allow", "allow"), ("Deny", "deny"), ("Drop (silent)", "drop"))
