# FQDN

Fully qualified domain name, can be used on some firewalls in place of a static IP(s).

## Attributes

* Name (string)
* Description (optional, string)
* IP Addresses (M2M to IPAddress)
    * Not required
    * Should be used if a firewall needs to tie a FQDN to an IP instead of on evaluating the FQDN to an IP when enforcing the PolicyRule.
* Status (FK to Status)
