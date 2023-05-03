# NATPolicyRule

Represents a single network address translation rule in a NATPolicy.

It is recommended to use a descriptive name to best identify a NATPolicyRule, otherwise the string representation of the NATPolicyRule will be the UUID.

## Attributes

### Meta information

* Name (optional, string)
* Status (FK to Status)
* Tags (M2M to Tag)
* Source Zone (FK to Zone)
* Source Zone (FK to Zone)
* Request ID (optional, string)
    * Meant to represent an upstream request (e.g. an service request from an ITSM solution).
* Index (optional, int)
    * Sets the index of the PolicyRule in the Policy.
    * Example `20 permit icmp host 1.1.1.1 any` would have an index of `20`.
    * Set as optional for now, will be set to required at a later date with default as the highest value + 10.
* Log (boolean)

### Before translation

* Original Source Address (M2M to AddressObject)
* Original Source Address Group (M2M to AddressObjectGroup)
* Original Destination Address (M2M to AddressObject)
* Original Destination Address Group (M2M to AddressObjectGroup)
* Original Source Service (M2M to ServiceObject)
* Original Source Service Group (M2M to ServiceObjectGroup)
* Original Destination Service (M2M to ServiceObject)
* Original Destination Service Group (M2M to ServiceObjectGroup)

### After translation

* Translated Source Address (M2M to AddressObject)
* Translated Source Address Group (M2M to AddressObjectGroup)
* Translated Destination Address (M2M to AddressObject)
* Translated Destination Address Group (M2M to AddressObjectGroup)
* Translated Source Service (M2M to ServiceObject)
* Translated Source Service Group (M2M to ServiceObjectGroup)
* Translated Destination Service (M2M to ServiceObject)
* Translated Destination Service Group (M2M to ServiceObjectGroup)
