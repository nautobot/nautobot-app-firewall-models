# v2.0 Release Notes

This document describes all new features and changes in the release `2.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v2.0.3 (2024-01-08)

### Changed

- [#202](https://github.com/nautobot/nautobot/issues/202) - Replaced `pydocstyle` with `ruff`.

### Fixed

- [#203](https://github.com/nautobot/nautobot/issues/203) - Fixed old reference to class path in URL pattern for job.

## v2.0.2 - 2024-01-04

### Fixed

- [#199](https://github.com/nautobot/nautobot-app-firewall-models/issues/199) Resolve incorrect reverse for custom viewset

### Added

- [#199](https://github.com/nautobot/nautobot-app-firewall-models/issues/199) Added towncrier changelogs

### Changed

- [#195](https://github.com/nautobot/nautobot-app-firewall-models/pull/195) Replace references to `plugin` with `app`

## v2.0.1 - 2023-10-04

### Fixed

- [#173](https://github.com/nautobot/nautobot-app-firewall-models/issues/173) Resolve issues with v2 migrations

## v2.0.0 - 2023-09-29

### Changed

- [#167](https://github.com/nautobot/nautobot-app-firewall-models/pull/167) Nautobot 2.0.0 as minimum dependency
- [#167](https://github.com/nautobot/nautobot-app-firewall-models/pull/167) Substantial updates to API
- [#167](https://github.com/nautobot/nautobot-app-firewall-models/pull/167) on_delete=PROTECT was moved from the model custom through field to a DB signal

### Added

- [#167](https://github.com/nautobot/nautobot-app-firewall-models/pull/167) Added support for Python 3.11

### Removed

- [#167](https://github.com/nautobot/nautobot-app-firewall-models/pull/167) Dropped support for Python 3.7
