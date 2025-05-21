# v2.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release adds support for Python 3.12.

## [v2.2.0 (2024-11-05)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v2.2.0)

### Added

- [#266](https://github.com/nautobot/nautobot-app-firewall-models/issues/266) - Added Python 3.12 support.

### Fixed

- [#222](https://github.com/nautobot/nautobot-app-firewall-models/issues/222) - Fixed server error when navigating to Policy detail view.
- [#233](https://github.com/nautobot/nautobot-app-firewall-models/issues/233) - Fixed name fields being optional on multiple forms.
- [#233](https://github.com/nautobot/nautobot-app-firewall-models/issues/233) - Fixed assigned devices and assigned dynamic groups fields not marked as optional on NATPolicy and Policy.
- [#245](https://github.com/nautobot/nautobot-app-firewall-models/issues/245) - Fixed server error when navigating to NATPolicy detail view.
- [#245](https://github.com/nautobot/nautobot-app-firewall-models/issues/245) - Fixed server error when updating device/dynamic group weights on NATPolicy.
- [#272](https://github.com/nautobot/nautobot-app-firewall-models/issues/272) - Fixed migrations failing when no statuses exist in the database and various other migration issues.
- [#275](https://github.com/nautobot/nautobot-app-firewall-models/issues/275) - Fixed capirca failures with Nautobot v2.3.3 or higher.
- [#280](https://github.com/nautobot/nautobot-app-firewall-models/issues/280) - Fixed Capirca policy html templates.

### Housekeeping

- [#281](https://github.com/nautobot/nautobot-app-firewall-models/issues/281) - Changed model_class_name in .cookiecutter.json to a valid model to help with drift management.


## [v2.2.1 (2025-01-16)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v2.2.1)

### Removed

- [#269](https://github.com/nautobot/nautobot-app-firewall-models/issues/269) - Removed the filter_address method from IPRangeFilterSet to resolve issues with searching for IPRange objects through the GUI and API.

### Housekeeping

- [#1](https://github.com/nautobot/nautobot-app-firewall-models/issues/1) - Rebaked from the cookie `nautobot-app-v2.4.1`.
