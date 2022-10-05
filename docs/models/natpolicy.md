# NATPolicy

A `NATPolicy` models a set of network address translation (NAT) rules. NAT Policies are assigned to Devices and Dynamic Groups.

## Attributes

* Name (string)
* Description (optional, string)
* NAT Policy Rules (M2M to NATPolicyRule via NATPolicyRuleM2M)
* Assigned Devices (M2M to Device via NATPolicyDeviceM2M)
    * Assigns a `NATPolicy` to a Device
* Assigned Dynamic Groups (M2M to DynamicGroup via NATPolicyDynamicGroupM2M)
    * Assigns a Policy to a `[DynamicGroup]`(https://nautobot.readthedocs.io/en/stable/additional-features/dynamic-groups/) which can then be used to dynamically assign to a Device/VirtualMachine or set of Devices/VirtualMachines
* Status (FK to `Status`)
* Tags (M2M to `Tag`)
