# PolicyDynamicGroupM2M

Allows for creating a weighted value affecting how a Policy is assigned to a Dynamic Group.

This model is not directly exposed to the user but is exposed through the Policy object and the weight is set via the Policy detail view.

## Attributes

* Weight (int, default=100)
    * Meant to allow for setting priority on how a Policy is applied to a Device.
    * Weight is not required to be unique.
    * Weight is not required to be used if not needed.
* Policy (FK to Policy)
* Dynamic Groups (FK to DynamicGroup)
