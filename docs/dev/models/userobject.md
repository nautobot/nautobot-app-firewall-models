# UserObject

Defines a User and is NOT related to a user in Nautobot. User Object is commonly used to identify a source for traffic on networks with roaming users.

## Attributes

* Name (optional, string)
    * Signifies the name of the user, commonly first and last name (e.g. John Smith).
    * Most likely would not be used in a policy but as a helper to identify an object.
* Username (string)
    * Signifies the username in identity provider (e.g. john.smith).
* Status (FK to Status)
