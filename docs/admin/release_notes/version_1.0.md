# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Major features or milestones
- Achieved in this `x.y` release
- Changes to compatibility with Nautobot and/or other apps, libraries etc.

## [v1.0.1] - 2021-09-08

### Added

### Changed

### Fixed

- [#123](https://github.com/nautobot/nautobot-app-firewall-models/issues/123) Fixed Tag filtering not working in job launch form

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
