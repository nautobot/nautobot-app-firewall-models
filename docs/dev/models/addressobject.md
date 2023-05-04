# AddressObject

Defines an object representation of some form of an IP object for cleaner nesting and modeling. Each Address Object can have only ONE IP object type associated to it. The Address property will return the IP object related to the Address Object (e.g. if FQDN is set, `instance.address` would return the FQDN object).

## Attributes

* Name (string)
* Description (optional, string)
* FQDN (FK to FQDN)
* IP Range (FK to IPRange)
* IP Address (FK to IPAddress)
* Prefix (FK to Prefix)
* Status (FK to Status)
* Address (property that returns the assigned object)
