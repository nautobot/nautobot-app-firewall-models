# IPRange

Tracks ranges of IP addresses, it is NOT represented in the IPAM objects in Nautobot and is ONLY used inside the plugin.

## Attributes

* Description (optional, string)
* Start Address (IPv4 OR IPv6)
* End Address (IPv4 OR IPv6)
* VRF (optional, FK to VRF)
* Size (int, automatically set)
* Status (FK to Status)
