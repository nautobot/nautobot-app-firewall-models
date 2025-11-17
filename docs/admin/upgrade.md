# Upgrading the App

Here you will find any steps necessary to upgrade the App in your Nautobot environment.

## Upgrade Nautobot 1.X to Nautobot 2.X

As part of the upgrade for Nautobot 2.0 it is recommended to perform a stepped upgrade by first upgrading Nautobot the lastest stable release within these constraints `>=1.6.2,<2.0.0`. After performing the initial upgrade of Nautobot you will need to run `nautobot-server populate_platform_network_driver --no-use-napalm-driver-field`. This will populate the `network_driver` attribute on Platform objects from the `slug` field.

## Upgrade Guide

When a new release comes out it may be necessary to run a migration of the database to account for any changes in the data models used by this app. Execute the command `nautobot-server post-upgrade` within the runtime environment of your Nautobot installation after updating the `nautobot-firewall-models` package via `pip`.

## Migrating CapircaPolicy to FirewallConfig

If you are upgrading from a version of `nautobot-firewall-models` that used the `CapircaPolicy` model to a version that uses the new `FirewallConfig` model, you must migrate your data using the provided management command. This allows both models to coexist and lets you migrate at your convenience. In 3.0, the `CapircaPolicy` model will be removed, but in the meantime both integrations can co-exist.

### Migration Steps

1. **Check your platform compatibility**

	Update the platforms `network_driver` and associated `network_driver_mappings["capirca"]` to match the `CAPIRCA_MAPPER`. It will not be migrated otherwise. The current Capirca model supports both, so you can transition.

1. **Set your default driver**

    Set the `default_driver` setting to match your expectation to one of 'aerleon', 'capirca', or 'custom_firewall_config'. This will be used in the migration script as well as your default when creating a new one.

1. **Review migration command:**

	The app provides a management command to migrate data from `CapircaPolicy` to `FirewallConfig`:
	```sh
	nautobot-server capirca_to_fw_config_migration
	```
	By default, this command runs in dry-run mode and will not write any changes. It will log what would be migrated and what would be skipped.

1. **Perform the migration:**

	When you are ready to migrate, run the command with the `--commit` flag:
	```sh
	nautobot-server capirca_to_fw_config_migration --commit
	```
	This will migrate all eligible `CapircaPolicy` records to `FirewallConfig`. Policies that do not meet all of the requirements will be skipped and logged.

1. **Verify migration:**

	Review the output and verify that your data has been migrated as expected. Skipped records will be reported in the output. You can safely re-run the migration command; already-migrated records will be skipped.

1. **Delete CapircaPolicy objects:**

	Once you have verified that all necessary data has been migrated, delete the records from `CapircaPolicy` model, likely using the bulk delete option. The migration in 3.x will require the data model to be empty.

1. **Optionally switch to Aerleon:**

	If you wish to use Aerleon as your policy generator, you can bulk edit the `FirewallConfig` objects. Additionally, the new pattern allows you to set custom on a per device basis.

!!! tip
    - The migration command ensures that only policies with a valid new-style platform mapping are migrated. Others are skipped and logged.
    - You can run the migration command multiple times; already-migrated records will be skipped.
    - Always back up your database before performing migrations.
