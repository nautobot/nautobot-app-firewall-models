# Upgrading the App

Here you will find any steps necessary to upgrade the App in your Nautobot environment.

## Upgrade Nautobot 1.X to Nautobot 2.X

As part of the upgrade for Nautobot 2.0 it is recommended to perform a stepped upgrade by first upgrading Nautobot the lastest stable release within these constraints `>=1.6.2,<2.0.0`. After performing the initial upgrade of Nautobot you will need to run `nautobot-server populate_platform_network_driver --no-use-napalm-driver-field`. This will populate the `network_driver` attribute on Platform objects from the `slug` field.

## Upgrade Guide

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this app. Execute the command `nautobot-server post-upgrade` within the runtime environment of your Nautobot installation after updating the `nautobot-firewall-models` package via `pip`.

## Migrating from Capirca to Aerleon

Previous versions of nautobot-firewall-app used Capirca as their backend for firewall configuration generation.
Please make sure to follow the steps below while migrating from a version of this app which used Capirca
as a backend (latest is v2.2.2) to the newest version with Aerleon:

* Reinstall dependencies.
* Migrate your `nautobot_config.py`. Configuration keys with `capirca_` prefix have been renamed to `aerleon_`.
* Run database migrations as usual.

There are no breaking changes between Capirca and Aerleon generators. Normally you should not have to change any
firewall rules and/or policies.
