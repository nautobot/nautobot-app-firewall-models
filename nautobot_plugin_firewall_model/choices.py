"""Set of choices to use in firewall models."""

from django.db.models import Q
from netutils.protocol_mapper import PROTO_NAME_TO_NUM


IP_PROTOCOL_CHOICES = ((i, i) for i in PROTO_NAME_TO_NUM.keys())

ADDRESS_ASSIGNMENT_MODELS = Q(
    Q(app_label="ipam", model="ipaddress")
    | Q(app_label="ipam", model="prefix")
    | Q(app_label="nautobot_plugin_firewall_model", model="iprange")
    | Q(app_label="nautobot_plugin_firewall_model", model="addressgroup")
    | Q(app_label="nautobot_plugin_firewall_model", model="fqdn")
)

USER_ASSIGNMENT_MODELS = Q(
    Q(app_label="nautobot_plugin_firewall_model", model="user")
    | Q(app_label="nautobot_plugin_firewall_model", model="usergroup")
)

SERVICE_ASSIGNMENT_MODELS = Q(
    Q(app_label="nautobot_plugin_firewall_model", model="protocol")
    | Q(app_label="nautobot_plugin_firewall_model", model="servicegroup")
)

ACTION_CHOICES = (("Allow", "allow"), ("Deny", "deny"), ("Drop (silent)", "drop"))
