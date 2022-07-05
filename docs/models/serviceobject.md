# ServiceObject

Service Object represents a single destination service.

For well-known ports, it is best to use the port name as the name of the object. For example, a service called `HTTP` should be TCP 80. A non-standard service 8898 serving HTTP traffic could be called `HTTP-8898` or `HTTP-SomeDescriptorForService`.

## Attributes

* Name (string)
* Description (optional, string)
* Port (optional, int OR int range)
    * Must be specified as a valid layer 4 port OR port range (e.g. 80 OR 8080-8088).
* IP Protocol (string, choice field)
    * IANA protocols (e.g. TCP UDP ICMP)
* Status (FK to Status)
