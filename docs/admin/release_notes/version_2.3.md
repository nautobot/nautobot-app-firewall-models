
# v2.3 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Dropped support for Python 3.8 and Python 3.9.0 - 3.9.1.
- Changed minimum Nautobot version to 2.4.2.

## [v2.3.0 (2025-09-25)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v2.3.0)

### Removed

- [#318](https://github.com/nautobot/nautobot-app-firewall-models/issues/318) - Dropped support for Python 3.8 and Python 3.9.0 - 3.9.1.

### Changed

- [#318](https://github.com/nautobot/nautobot-app-firewall-models/issues/318) - Changed minimum Nautobot version to 2.4.2.

### Fixed

- [#293](https://github.com/nautobot/nautobot-app-firewall-models/issues/293) - Removed incorrect config context model forms from all forms.
- [#295](https://github.com/nautobot/nautobot-app-firewall-models/issues/295) - Standardized the object description fields to max 1024 characters and all other charfields to max 255 characters.
- [#320](https://github.com/nautobot/nautobot-app-firewall-models/issues/320) - Fixed the reference of addresses in address groups with complex names.

### Dependencies

- [#318](https://github.com/nautobot/nautobot-app-firewall-models/issues/318) - Pinned Django debug toolbar to <6.0.0.

### Housekeeping

- Rebaked from the cookie `nautobot-app-v2.5.1`.
- Rebaked from the cookie `nautobot-app-v2.6.0`.
