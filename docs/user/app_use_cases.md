# Using the App

This document describes common use-cases and scenarios for this App.

## General Usage

A detailed walkthrough is provided in the [Introducing Nautobot Firewall Models](https://blog.networktocode.com/post/nautobot-firewall-models/) blog post.

### Assigning Policies

There are three primary ways of assigning policies (`Policy` or `NATPolicy` objects) to devices:

- Directly via the `assigned_devices` attribute on a policy object.
- Dynamically by assigning an existing `DynamicGroup` object to the `assigned_dynamic_groups` field on a policy object.
- By creating a new `Relationship` specifying additional targets for policy association. This can be, for example, used to associate a policy with an `Interface` object.
    + The use of a Relationship _may_ limit future integrations with parsing or templating.

Although policies can be created without any rules it is recommended to create the required underlying objects first before moving to the policy definitions. [Creation Order](../dev/models.md#creation-order) provides an ordered list of steps for creating and assigning, objects, needed for policy creation.

## Use-cases and common workflows

For examples of REST and GraphQL API usage see the [External Interactions](external_interactions.md) page.

Should you wish to integrate Nautobot data with firewall configuration policies, please read the [Aerleon Integration](aerleon.md) page.

## Screenshots

![Navigation Menu](../images/navmenu.png "Navigation Menu")

![Policy View](../images/policy.png "Policy View")
