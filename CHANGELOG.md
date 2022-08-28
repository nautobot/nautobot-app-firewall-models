# Changelog

## v1.0.0 - 2022-08-27

### Removed

- #80 Support for Nautobot < v1.4.0

### Changed

- #80 All plural attrs on PolicyRule are now represented in plural form (`source_user` is now `source_users` etc).
- #80 Nav menu name from `Firewall` to `Security`.
- #80 Styling on PolicyRule detail tables

### Added

- #80 Support for Notes
- #80 Source Service suport
- #80 Security panel on homepage
- #80 PolicyRule detail tables convert empty value to `ANY`

## v0.1.0-beta.3 - 2022-07-19

### Changed

- #68 Update Policy Rules Expanded to be more intuitive
- #69 Change to use arrow in UI elements

### Added

- #63 Capirca Integration

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
