"""Constants file."""

from django.conf import settings

# This is used to map the slug of the platform in the customers environment to the expected name that Aerleon is looking for
AERLEON_OS_MAPPER = {}

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {})

if PLUGIN_CFG.get("aerleon_os_map"):
    AERLEON_OS_MAPPER = PLUGIN_CFG["aerleon_os_map"]

# This is used to determine which status slug names are valid
ALLOW_STATUS = ["Active"]
if PLUGIN_CFG.get("allowed_status"):
    ALLOW_STATUS = PLUGIN_CFG["allowed_status"]

# This is used to whitelist actions that align with Aerleon
ACTION_MAP = {"allow": "accept", "deny": "deny", "drop": "reject"}  # no next or reject-with-tcp-rst
# This is used to transpose string booleans to Aerleon expectations
LOGGING_MAP = {"true": "true", "false": "disable"}

# This is used to provide hints (for type), and dotted string back (for lib) to Aerleon
AERLEON_MAPPER = {
    "arista": {
        "lib": "aerleon.lib.arista.Arista",
        "type": "filter-name",
    },
    "aruba": {
        "lib": "aerleon.lib.aruba.Aruba",
        "type": "filter-name",
    },
    "brocade": {
        "lib": "aerleon.lib.brocade.Brocade",
        "type": "filter-name",
    },
    "cisco": {
        "lib": "aerleon.lib.cisco.Cisco",
        "type": "filter-name",
    },
    "ciscoasa": {
        "lib": "aerleon.lib.ciscoasa.CiscoASA",
        "type": "filter-name",
    },
    "cisconx": {
        "lib": "aerleon.lib.cisconx.ciscoNX",
        "type": "filter-name",
    },
    "cloudarmor": {
        "lib": "aerleon.lib.cloudarmor.CloudArmor",
        "type": "filter_type",
    },
    "gce": {
        "lib": "aerleon.lib.gce.GCE",
        "type": "filter-name",
    },
    "gcp_hf": {
        "lib": "aerleon.lib.gcp.GCP",
        "type": "filter-name",
    },
    "ipset": {
        "lib": "aerleon.lib.ipset.Ipset",
        "type": "direction",
    },
    "iptables": {
        "lib": "aerleon.lib.iptables.Iptables",
        "type": "direction",
    },
    "juniper": {
        "lib": "aerleon.lib.juniper.Juniper",
        "type": "filter-name",
    },
    "juniperevo": {
        "lib": "aerleon.lib.juniperevo.JuniperEvo",
        "type": "filter-name",
    },
    "junipermsmpc": {
        "lib": "aerleon.lib.junipermsmpc.JuniperMSMPC",
        "type": "filter-name",
    },
    "srx": {
        "lib": "aerleon.lib.junipersrx.JuniperSRX",
        "type": "zone",
    },
    "k8s": {
        "lib": "aerleon.lib.k8s.K8s",
        "type": "direction",
    },
    "nftables": {
        "lib": "aerleon.lib.nftables.Nftables",
        "type": "address_family",
    },
    "nsxv": {
        "lib": "aerleon.lib.nsxv.Nsxv",
        "type": "filter-name",
    },
    "packetfilter": {
        "lib": "aerleon.lib.packetfilter.PacketFilter",
        "type": "filter-name",
    },
    "paloalto": {
        "lib": "aerleon.lib.paloaltofw.PaloAltoFW",
        "type": "zone",
    },
    "pcap": {
        "lib": "aerleon.lib.pcap.PcapFilter",
        "type": "filter-name",
    },
    "speedway": {
        "lib": "aerleon.lib.speedway.Speedway",
        "type": "direction",
    },
    "srxlo": {
        "lib": "aerleon.lib.srxlo.SRXlo",
        "type": "filter-name",
    },
    "windows_advfirewall": {
        "lib": "aerleon.lib.windows_advfirewall.WindowsAdvFirewall",
        "type": "direction",
    },
    "windows_ipsec": {
        "lib": "aerleon.lib.windows_ipsec.WindowsIPSec",
        "type": "filter-name",
    },
}
