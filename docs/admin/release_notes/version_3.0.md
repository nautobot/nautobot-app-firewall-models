# v3.0 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This major release marks the compatibility of the Firewall Models App with Nautobot 3.0.0. Check out the [full details](https://docs.nautobot.com/projects/core/en/stable/release-notes/version-3.0/) of the changes included in this new major release of Nautobot. Highlights:

- Minimum Nautobot version supported is 3.0.
- Added support for Python 3.13 and removed support for 3.9.
- Updated UI framework to use latest Bootstrap 5.3.

We will continue to support the previous major release for users of Nautobot LTM 2.4 only with critical bug and security fixes as per the [Software Lifecycle Policy](https://networktocode.com/company/legal/software-lifecycle-policy/).

<!-- towncrier release notes start -->

## [v3.0.0 (2025-11-17)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v3.0.0)

### Added

- Added support for Nautobot 3.0.
- Added support for Python 3.13.

### Change

### Fixed

- [#332](https://github.com/nautobot/nautobot-app-firewall-models/issues/332) - Fixed several places where rendering of `verbose_name` was incorrect.
- [#349](https://github.com/nautobot/nautobot-app-firewall-models/issues/349) - Fixed the filter used in the Address Object panel badge link on the Address Object Group detail page.
- [#349](https://github.com/nautobot/nautobot-app-firewall-models/issues/349) - Fixed the filter used in the Application Object panel badge link on the Application Object Group detail page.
- [#350](https://github.com/nautobot/nautobot-app-firewall-models/issues/350) - Fixed permissions on edit device weight and edit dynamic group weight tabs for Policy and NATPolicy.
- [#352](https://github.com/nautobot/nautobot-app-firewall-models/issues/352) - Added size field to IPRange detail view.

## [v3.0.0a1 (2025-11-05)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v3.0.0a1)
