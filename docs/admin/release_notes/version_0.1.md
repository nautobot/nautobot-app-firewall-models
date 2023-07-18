# v0.1 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.1.0-beta.3 - 2022-07-19

### Changed

- `#68` Update Policy Rules Expanded to be more intuitive
- `#69` Change to use arrow in UI element

### Added

- [#63](https://github.com/nautobot/nautobot-plugin-firewall-models/issues/63) Capirca Integration

## v0.1.0-beta.2 - 2022-07-10

### Changed

- Update Serializers to current standards
- Update development environment to current standards
- Update CI matrix for better runtime & coverage of versions

### Fixed

- Pydocstyle.ini being properly used
- Dockerfile to work with `NAUTOBOT_VER` from build args, previously poetry superceeded the build arg.
- Updates for `status` attributes to account for defaulting.
- Static URLs for images in `README.md` to fix broken link in PyPI page rendering.

### Added

- Ability to expand Policy detail API view with query param `deep=True`.
- Added `to_json` method on `Policy` and `PolicyRule` models.
- Added `rule_details` as a helper for working with a `PolicyRule`
- Added `policy_details` as a helper for working with a `Policy`
- Initial scaffolding for `MySQL` development environment support.

## v0.1.0-beta.1 - 2022-07-08

### Fixed

- Issues with docs rendering in PyPI & ReadTheDocs

## v0.1.0-beta.2 - 2022-07-08

### Announcements

- Initial Release
