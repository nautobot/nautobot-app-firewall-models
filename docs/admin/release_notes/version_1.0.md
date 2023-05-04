# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.0.2 - 2022-09-22

### Fixed

- [#87](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/87) NestedWritabeSerializer fix for schema generation on VarBinaryField
- [#88](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/88) Docs fix
- [#89](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/89) Ressolve ordering when viewing PolicyRules via a Policy view.

## v1.0.1 - 2022-09-18

### Fixed

- [#84](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/84) Missing Index from PolicyRule form.
- [#84](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/84) Missing Source/Destination descriptors on Service/Service Group for PolicyRule form.

## v1.0.0 - 2022-08-27

### Removed

- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Support for Nautobot < v1.4.0

### Changed

- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) All plural attrs on PolicyRule are now represented in plural form (`source_user` is now `source_users` etc).
- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Nav menu name from `Firewall` to `Security`.
- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Styling on PolicyRule detail tables

### Added

- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Support for Notes
- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Source Service suport
- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) Security panel on homepage
- [#80](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/80) PolicyRule detail tables convert empty value to `ANY`
