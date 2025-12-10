# v2.4 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Change minimum Nautobot version to 2.4.20.
- Dropped support for Python 3.9.
- Several bug fixes and improvements.

<!-- towncrier release notes start -->
## [v2.4.0 (2025-12-09)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v2.4.0)

### Fixed

- [#332](https://github.com/nautobot/nautobot-app-firewall-models/issues/332) - Fixed several places where rendering of `verbose_name` was incorrect.
- [#357](https://github.com/nautobot/nautobot-app-firewall-models/issues/357) - Fixed permissions on edit device weight and edit dynamic group weight tabs for Policy and NATPolicy.
- [#360](https://github.com/nautobot/nautobot-app-firewall-models/issues/360) - Fixed an incompatibility when slugifying capirca names that start with a number by prefixing the name with an underscore.

### Dependencies

- [#332](https://github.com/nautobot/nautobot-app-firewall-models/issues/332) - Pinned Nautobot to 2.4.20 or greater to support several of the latest Nautobot UI Component updates.

### Housekeeping

- [#332](https://github.com/nautobot/nautobot-app-firewall-models/issues/332) - Fixed failing linting issues.
- [#332](https://github.com/nautobot/nautobot-app-firewall-models/issues/332) - Migrated all models to use the UI Component Framework.
- Rebaked from the cookie `nautobot-app-v2.7.0`.
- Rebaked from the cookie `nautobot-app-v2.7.1`.
- Rebaked from the cookie `nautobot-app-v2.7.2`.
