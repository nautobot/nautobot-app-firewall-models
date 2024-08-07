# v2.1 Release Notes

This document describes all new features and changes in the release `2.1`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

This release includes various housekeeping updates and adds support for Nautobot v2.3.0.

<!-- towncrier release notes start -->
## [v2.1.0 (2024-08-07)](https://github.com/nautobot/nautobot-app-firewall-models/releases/tag/v2.1.0)

### Added

- [#213](https://github.com/nautobot/nautobot-app-firewall-models/issues/213) - Added `invoke generate-app-config-schema` command to generate a JSON schema for the App config.
- [#213](https://github.com/nautobot/nautobot-app-firewall-models/issues/213) - Added `invoke validate-app-config` command to validate the App config against the schema.
- [#213](https://github.com/nautobot/nautobot-app-firewall-models/issues/213) - Added App config JSON schema.
- [#258](https://github.com/nautobot/nautobot-app-firewall-models/issues/258) - Added migration to support Django 4.

### Fixed

- [#258](https://github.com/nautobot/nautobot-app-firewall-models/issues/258) - Fixed IPRangeSerializer requiring vrf field.

### Housekeeping

- [#8](https://github.com/nautobot/nautobot-app-firewall-models/issues/8), [#229](https://github.com/nautobot/nautobot-app-firewall-models/issues/229) - Re-baked from the latest template.
- [#212](https://github.com/nautobot/nautobot-app-firewall-models/issues/212) - Fixed ruff excludes to use per-file excludes instead of global excludes.
- [#218](https://github.com/nautobot/nautobot-app-firewall-models/issues/218) - Rebaked using `nautobot-app-v2.1.0` cookiecutter template tag.
