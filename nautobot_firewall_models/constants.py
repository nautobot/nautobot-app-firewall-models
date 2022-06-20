from django.conf import settings

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("nautobot_firewall_models", {})
CAPIRCA_OS_MAPPER = {}

if PLUGIN_CFG.get("capirca_mapping"):
    CAPIRCA_OS_MAPPER = PLUGIN_CFG["capirca_mapping"]

ACTION_MAP = {"allow": "accept", "deny": "deny", "drop": "reject"}  # no next or reject-with-tcp-rst
LOGGING_MAP = {"true": "true", "false": "disable"}

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
    "junipersrx": {
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
