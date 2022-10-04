# NATPolicyDeviceM2M

Allows for creating a weighted value affecting how a NATPolicy is assigned to a Device.

This model is not directly exposed to the user but can be accessed via the NATPolicy object, and the weight value is set in the NATPolicy detail view.

## Attributes

* Weight (int, default=100)
    * Meant to allow for setting priority on how a NATPolicy is applied to a Device.
    * Weight is not required to be unique.
    * Weight is not required to be used if not needed.
* NATPolicy (FK to NATPolicy)
* Devices (FK to Device)
