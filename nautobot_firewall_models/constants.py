"""Constants file."""

from django.conf import settings

# This is used to map the slug of the platform in the customers environment to the expected name that Capirca is looking for

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {})


CAPIRCA_OS_MAPPER = {}
if PLUGIN_CFG.get("capirca_os_map"):
    CAPIRCA_OS_MAPPER = PLUGIN_CFG["capirca_os_map"]


FIREWALL_CONFIG_OS_MAPPER = {}
if PLUGIN_CFG.get("firewall_config_os_map"):
    FIREWALL_CONFIG_OS_MAPPER = PLUGIN_CFG["firewall_config_os_map"]

# This is used to determine which status slug names are valid
ALLOW_STATUS = ["Active"]
if PLUGIN_CFG.get("allowed_status"):
    ALLOW_STATUS = PLUGIN_CFG["allowed_status"]

# This is used to whitelist actions that align with Capirca
ACTION_MAP = {"allow": "accept", "deny": "deny", "drop": "reject"}  # no next or reject-with-tcp-rst
# This is used to transpose string booleans to Capirca expectations
LOGGING_MAP = {"true": "true", "false": "disable"}

# This is used to provide hints (for type), and dotted string back (for lib) to Capirca
CAPIRCA_MAPPER = {
    "arista": {
        "lib": "capirca.lib.arista.Arista",
        "type": "filter-name",
    },
    "aruba": {
        "lib": "capirca.lib.aruba.Aruba",
        "type": "filter-name",
    },
    "brocade": {
        "lib": "capirca.lib.brocade.Brocade",
        "type": "filter-name",
    },
    "cisco": {
        "lib": "capirca.lib.cisco.Cisco",
        "type": "filter-name",
    },
    "ciscoasa": {
        "lib": "capirca.lib.ciscoasa.CiscoASA",
        "type": "filter-name",
    },
    "cisconx": {
        "lib": "capirca.lib.cisconx.ciscoNX",
        "type": "filter-name",
    },
    "cloudarmor": {
        "lib": "capirca.lib.cloudarmor.CloudArmor",
        "type": "filter_type",
    },
    "gce": {
        "lib": "capirca.lib.gce.GCE",
        "type": "filter-name",
    },
    "gcp_hf": {
        "lib": "capirca.lib.gcp.GCP",
        "type": "filter-name",
    },
    "ipset": {
        "lib": "capirca.lib.ipset.Ipset",
        "type": "direction",
    },
    "iptables": {
        "lib": "capirca.lib.iptables.Iptables",
        "type": "direction",
    },
    "juniper": {
        "lib": "capirca.lib.juniper.Juniper",
        "type": "filter-name",
    },
    "juniperevo": {
        "lib": "capirca.lib.juniperevo.JuniperEvo",
        "type": "filter-name",
    },
    "junipermsmpc": {
        "lib": "capirca.lib.junipermsmpc.JuniperMSMPC",
        "type": "filter-name",
    },
    "srx": {
        "lib": "capirca.lib.junipersrx.JuniperSRX",
        "type": "zone",
    },
    "k8s": {
        "lib": "capirca.lib.k8s.K8s",
        "type": "direction",
    },
    "nftables": {
        "lib": "capirca.lib.nftables.Nftables",
        "type": "address_family",
    },
    "nsxv": {
        "lib": "capirca.lib.nsxv.Nsxv",
        "type": "filter-name",
    },
    "packetfilter": {
        "lib": "capirca.lib.packetfilter.PacketFilter",
        "type": "filter-name",
    },
    "paloalto": {
        "lib": "capirca.lib.paloaltofw.PaloAltoFW",
        "type": "zone",
    },
    "pcap": {
        "lib": "capirca.lib.pcap.PcapFilter",
        "type": "filter-name",
    },
    "speedway": {
        "lib": "capirca.lib.speedway.Speedway",
        "type": "direction",
    },
    "srxlo": {
        "lib": "capirca.lib.srxlo.SRXlo",
        "type": "filter-name",
    },
    "windows_advfirewall": {
        "lib": "capirca.lib.windows_advfirewall.WindowsAdvFirewall",
        "type": "direction",
    },
    "windows_ipsec": {
        "lib": "capirca.lib.windows_ipsec.WindowsIPSec",
        "type": "filter-name",
    },
}

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
    "fortigate": {
        "lib": "aerleon.lib.fortigate.Fortigate",
        "type": "zone",
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
    "proxmox": {
        "lib": "aerleon.lib.proxmox.Proxmox",
        "type": "direction",
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
