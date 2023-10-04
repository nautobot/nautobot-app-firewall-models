# v2.0 Release Notes

This document describes all new features and changes in the release `2.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v2.0.1 - 2023-10-04

### Fixed

- [#173](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/173) Resolve issues with v2 migrations

## v2.0.0 - 2023-09-29

### Changed

- [#167](https://github.com/nautobot/nautobot-plugin-firewall-models/pull/167) Nautobot 2.0.0 as minimum dependency
- [#167](https://github.com/nautobot/nautobot-plugin-firewall-models/pull/167) Substantial updates to API
- [#167](https://github.com/nautobot/nautobot-plugin-firewall-models/pull/167) on_delete=PROTECT was moved from the model custom through field to a DB signal

### Added

- [#167](https://github.com/nautobot/nautobot-plugin-firewall-models/pull/167) Added support for Python 3.11

### Removed

- [#167](https://github.com/nautobot/nautobot-plugin-firewall-models/pull/167) Dropped support for Python 3.7
