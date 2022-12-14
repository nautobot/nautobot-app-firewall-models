# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.1.3 - 2022-11-16

### Fixed

- `#114` Resolved issues with status filters & deep=True method on Policy detail API view

## v1.1.2 - 2022-11-12

### Added

- `#108` Enable cloning for PolicyRule and NATPolicyRule models
- `#110` Add support for port lists on ServiceObject

### Fixed

- `#109` Resolved incorrect links in mkdocs.yml

## v1.1.1 - 2022-10-26

### Fixed

- `#99` Remove creation of extraneous status content types during migrations
- `#100` Force Poetry to package the static documentation

### Added

- `#103` Add request_id and description as available fields for the rule tables

### Changed

- `#104` Enable brief endpoint API testing for supported models

## v1.1.0 - 2022-10-04

### Fixed

- `#93` Updated Capirca Documentation syntax
- `#95` Updated CI to cancel previous run on new commit to same branch

### Added

- `#92` Initial Addition of NAT models

