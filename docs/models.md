# Models

Modeling firewall objects can be quite complex and to provide as much flexibility as possible a nest approach has been taken. To also avoid downstream objects from being removed from Nautobot that then causes unexpected changes to a firewall policy EVERY many to many relationship is set so the child object cannot be deleted if it is used by a parent. For example an IPAddress used in an AddressObject that follows up the chain into a Policy, if someone was to try and delete this IPAddress Nautobot will prevent this from happening until either the relationship to the AddressObject is removed OR the AddressObject is deleted. This is to enforce a deliberate approach to managing objects and that you must first remove the object from it's parent before it can be deleted. In the below diagram you will see all models depicted and the furthest left if the most "parent" object with the each relationship that cascades down is a child of the parent to the left.

All the data models introduced by the Firewall plugin support the following Nautobot features:

* Rest API
* GraphQL
* Custom fields
* Custom Links
* Relationships
* Change logging
* Custom data validation logic
* Webhooks

<p align="center">
  <img src="./images/datamodel.png" class="center">
</p>

## Creation Order

With all the nested relationship to manage it is easiest to work from the right to the left of the diagram in creation.

1. Create the "end objects" AddressObjects UserObjects and ServiceObjects
    * For AddressObjects first create the underlying objects to use in creating the AddressObject (i.e. create IPAddress before attempting to create an AddressObject for that IP).
2. Create groups if needed, AddressObjectGroups UserObjectGroups and ServiceObjectGroups
    * Groups are not required but are commonly used to group like objects together in firewall policies.
3. Create PolicyRules
4. Create Policy & assign indexes to rules.
5. Add Device and/or DynamicGroup objects to a Policy

## Custom Through Models

This plugin heavily employs the use of [custom through models](https://docs.djangoproject.com/en/3.2/howto/custom-model-fields/) for both disabling deleting from the bottom up AND for adding additional attributes that are only relevant in the relationship but not on the objects independently. 

`PolicyRuleM2M`, `PolicyDeviceM2M`, `PolicyDynamicGroupM2M` are used for setting additional attributes and the remainder are solely defined for the disabling deleting from the bottom up.

## Policy
A Policy is a collection of PolicyRules that are assigned to Devices and DynamicGroups. When used in the context of an access list a Policy is the full access list.

Example of access list that could be translated to a Policy
```no-highlight
Extended IP access list Virtual-Access1.1#1
    20 permit icmp host 1.1.1.1 any
    30 deny ip host 44.33.66.36 host 1.1.1.1
    40 permit udp any host 1.1.1.1
```

* Name (string)
* Description (optional, string)
* Policy Rules (M2M to PolicyRule via PolicyRuleM2M)
* Assigned Devices (M2M to Device via PolicyDeviceM2M)
    * Assigns a Policy to a Device
* Assigned Dynamic Groups (M2M to DynamicGroup via PolicyDynamicGroupM2M)
    * Assigns a Policy to a [DynamicGroup](https://nautobot.readthedocs.io/en/stable/additional-features/dynamic-groups/) which can then be used to dynamically assign to a Device/VirtualMachine or set of Devices/VirtualMachines
* Status (FK to Status)
* Tags (M2M to Tag)

## PolicyRuleM2M
Allows for creating an index value that is only relevant to the relationship, this allows for a PolicyRule to potentially be used multiple times across multiple Policies.

* Index (optional, int)
    * Sets the index of the PolicyRule in the Policy
    * Example `20 permit icmp host 1.1.1.1 any` would have an index of `20`
    * Must be unique
    * Set as optional for now, will be set to required at a later date with default as the highest value + 10.
        * Uniqueness does not apply when not set.
* Policy (FK to Policy)
* Policy Rules (FK to PolicyRule)

## PolicyDeviceM2M
Allows for created a weighted value on how a Policy is assigned to a Device.

* Weight (int, default=100)
    * Meant to allow for setting priority on how a Policy is applied to a Device.
    * Weight is not required to be unique.
    * Weight is not required to be used if not needed.
* Policy (FK to Policy)
* Devices (FK to Device)

## PolicyDynamicGroupM2M
Allows for created a weighted value on how a Policy is assigned to a DynamicGroup.

* Weight (int, default=100)
    * Meant to allow for setting priority on how a Policy is applied to a Device.
    * Weight is not required to be unique.
    * Weight is not required to be used if not needed.
* Policy (FK to Policy)
* Dynamic Groups (FK to DynamicGroup)

## PolicyRule
Represents a single line in a Policy.

Example line in an access list that would translate to a PolicyRule
```no-highlight
30 deny ip host 44.33.66.36 host 1.1.1.1
```

* Name (optional, string)
* Status (FK to Status)
* Tags (M2M to Tag)
* Source User (M2M to UserObject)
* Source User Group (M2M to UserObjectGroup)
* Source Address (M2M to AddressObject)
* Source Address Group (M2M to AddressObjectGroup)
* Source Zone (FK to Zone)
* Destination Address (M2M to AddressObject)
* Destination Address Group (M2M to AddressObjectGroup)
* Source Zone (FK to Zone)
* Service (M2M to ServiceObject)
* Service Group (M2M to ServiceObjectGroup)
* Action (string, choice of deny drop allow)
* Log (boolean)
* Request ID (optional, string)
    * Meant to represent an upstream request (i.e. an service request from an ITSM solution).

## ServiceObject
Represents a single destination service, if using a well known port it is recommended to use the port name as the name of the object. (i.e. a service called HTTP should be TCP 80, a non-standard service 8898 serving HTTP traffic may be best called `HTTP-8898` or `HTTP-SomeDescriptorForService`).

* Name (string)
* Description (optional, string)
* Port (optional, int OR int range)
    * Must be specified as a valid layer 4 port OR port range (i.e. 80 OR 8080-8088).
* IP Protocol (string, choice field)
    * IANA protocols (i.e. TCP UDP ICMP)
* Status (FK to Status)

## ServiceObjectGroup
Represents a group of ServiceObjects.

* Name (string)
* Description (optional, string)
* Service Objects (M2M to ServiceObject)
* Status (FK to Status)

## UserObject
Defines a User and is NOT related to a user of Nautobot, commonly used to identify a source for traffic on networks with roaming users.

* Name (optional, string)
    * Signifies the name of the user, commonly first & last name (i.e. John Smith)
    * Most likely would not be used in a policy but as a helper to identify an object
* Username (string)
    * Signifies the username in identify provider (i.e. john.smith)
* Status (FK to Status)

## UserObjectGroup
Represents a group of UserObjects.

* Name (string)
* Description (optional, string)
* User Objects (M2M to UserObject)
* Status (FK to Status)

## AddressObject
Defines an object representation of some form of an IP object for cleaner nesting and modeling. Each AddressObject can only have ONE IP object type associated to it. The Address property will return the related IP object to the AddressObject (i.e. if FQDN is set instance.address would return the FQDN object).

* Name (string)
* Description (optional, string)
* FQDN (FK to FQDN)
* IP Range (FK to IPRange)
* IP Address (FK to IPAddress)
* Prefix (FK to Prefix)
* Status (FK to Status)
* Address (property that returns the assigned object)

## AddressObjectGroup
Represents a group of AddressObjects.

* Name (string)
* Description (optional, string)
* Address Objects (M2M to AddressObject)
* Status (FK to Status)

## FQDN
Fully qualified domain name, can be used on some firewall in place of a static IP(s).

* Name (string)
* Description (optional, string)
* IP Addresses (M2M to IPAddress)
    * Not required
    * Should be used if a firewall needs to tie a FQDN to an IP instead of on process time
* Status (FK to Status)

## IPRange
Tracks ranges of IP addresses, is NOT represented in the IPAM objects in Nautobot and is ONLY used inside the plugin.

* Description (optional, string)
* Start Address (IPv4 OR IPv6)
* End Address (IPv4 OR IPv6)
* VRF (optional, FK to VRF)
* Size (int, automatically set)
* Status (FK to Status)

## Zone
Zones are common on firewalls and are typically seen as representations of area (i.e. DMZ trust untrust).

* Name (string)
* Description (optional, string)
* VRFs (M2M to VRF)
* Interfaces (M2M to Interface)
* Status (FK to Status)
