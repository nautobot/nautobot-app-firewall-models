# PolicyRuleM2M

Allows for creating an index value that is only relevant to the relationship, this allows for a Policy Rule to potentially be used multiple times across multiple Policies.

This model is not directly exposed to the user but can be accessed via the Policy object, and the index value is set in the Policy detail view.

## Attributes

* Index (optional, int)
    * Sets the index of the PolicyRule in the Policy.
    * Example `20 permit icmp host 1.1.1.1 any` would have an index of `20`.
    * Must be unique.
    * Set as optional for now, will be set to required at a later date with default as the highest value + 10.
        * Uniqueness does not apply when not set.
* Policy (FK to Policy)
* Policy Rules (FK to PolicyRule)
