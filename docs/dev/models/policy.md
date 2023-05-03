# Policy

A Policy models set of security rules permitting or blocking data packets.

Policy is defined as a collection of Policy Rules. Policies are assigned to Devices and Dynamic Groups.

You can think of a policy as roughly corresponding to access lists or policies on security appliances.

## Attributes

* Name (string)
* Description (optional, string)
* Policy Rules (M2M to PolicyRule via PolicyRuleM2M)
* Assigned Devices (M2M to Device via PolicyDeviceM2M)
    * Assigns a Policy to a Device
* Assigned Dynamic Groups (M2M to DynamicGroup via PolicyDynamicGroupM2M)
    * Assigns a Policy to a [DynamicGroup](https://nautobot.readthedocs.io/en/stable/additional-features/dynamic-groups/) which can then be used to dynamically assign to a Device/VirtualMachine or set of Devices/VirtualMachines
* Status (FK to Status)
* Tags (M2M to Tag)

## Examples

Example of access list that could be translated to a Policy

```no-highlight
Extended IP access list Virtual-Access1.1#1
    20 permit icmp host 1.1.1.1 any
    30 deny ip host 44.33.66.36 host 1.1.1.1
    40 permit udp any host 1.1.1.1
```
