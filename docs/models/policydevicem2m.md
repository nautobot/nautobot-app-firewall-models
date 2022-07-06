# PolicyDeviceM2M

Allows for creating a weighted value affecting how a Policy is assigned to a Device.

This model is not directly exposed to the user but can be accessed via the Policy object, and the weight value is set in the Policy detail view.

## Attributes

* Weight (int, default=100)
    * Meant to allow for setting priority on how a Policy is applied to a Device.
    * Weight is not required to be unique.
    * Weight is not required to be used if not needed.
* Policy (FK to Policy)
* Devices (FK to Device)
