# Usage
## Assigning Policies

There are three primary ways of assigning policies to devices:

* Directly via the `assigned_devices` attribute on the Policy object.
* Dynamically by assigning existing `DynamicGroup` object to the `assigned_dynamic_groups` on the Policy object.
    * At this time in Nautobot v1.3.X Dynamic Groups can only be assigned to Device objects or Virtual Machine objects.
* By creating a new `Relationship` specifying additional targets for Policy association. This can be, for example, used to associate Policy with an Interface object.
    * The use of a Relationship _may_ limit future integrations with parsing or templating.

Although policies can be created without any rules it is recommended to create the required underlying objects first before moving to the Policy definitions. [Creation Order](./models.md#creation-order) provides an ordered list of steps for creating and assigning, objects, needed for Policy creation.