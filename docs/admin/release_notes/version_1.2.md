# v1.2 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.2.1 - 2023-05-03

### Fixed

- [#135](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/135) Form fields incorrectly marked as required
- [#136](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/136) Invalid serializers for Zone and PolicyRule APIs
- [#145](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/145) FilterSets missing name field for PolicyRule and NATPolicyRule

### Changed

- [#140](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/140) Doc updates
- [#123](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/123) Doc updates

### Added

- [#143](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/143) Allow for ORM reversibility from CapircaPolicy

## v1.2.0 - 2023-02-08

### Fixed

- [#120](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/120) Resolved inconsistent forms.

### Changed

- [#108](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/108) Changed Application & Application Group migrations to allow null values.

### Added

- [#108](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/108) Application & ApplicationGroup support

## v1.2.0-alpha.2 - 2022-12-07

### Fixed

- [#120](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/120) Resolved inconsistent forms.

## v1.2.0-alpha.1 - 2022-11-25

### Changed

- [#108](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/108) Changed Application & Application Group migrations to allow null values.

## v1.2.0-alpha.0 - 2022-11-22

### Added

- [#108](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/108) Application & ApplicationGroup support

### Fixed

- [#117](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/117) Resolved `main` tab not loading on initial load of Policy & PolicyRule detail page

### Changed

- [#117](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/117) Reorganized `models/` folder to improve developer experience

