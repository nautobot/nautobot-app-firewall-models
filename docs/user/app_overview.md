# App Overview

This document provides an overview of the App including critical information and import considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

A plugin for [Nautobot](https://github.com/nautobot/nautobot) that is meant to model any of the following:

- Layer 4 firewall policies
- Extended access control lists
- NAT policies

Future development will include the ability to onboard an existing access list from a device and the ability to generate device configuration.

## Audience (User Personas) - Who should use this App?

This app will allow network and security engineers to model policies that drive their network and security automation. Even better, the firewall models are built to take a vendor-agnostic approach; the models are robust to provide maximum flexibility.

## Authors and Maintainers

Jeremy White @whitej6

## Nautobot Features Used

To view the models that are added to Nautobot please see the dedicated [models](../dev/models.md) page.
