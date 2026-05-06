# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.18.12] - 2026-05-06
### Added
- Add `URLParams` class in `query_params.py` to facilitate management
  of URL parameters with base64/JSON encoding.
- Add `URL_PARAMS` attribute to `URLParams` class for declarative
  configuration of query params.
- Add `has_url_params()` method to check if all required URL params
  are present.
- Add `get_url_params()` method to retrieve raw URL param values.
- Add `render_filters_section()` method to conditionally render the
  filter grid based on the presence of valid URL params.
- Add `encode_url_params()` and `decode_url_params()` utility methods
  for base64/JSON conversion.

### Changed
- No changes.

### Removed
- No changes.

## [0.18.7] - 2026-02-02
### Added
- Add codes to register dashboard service and route.

### Changed
- No changes.

### Removed
- Remove debug prints


## [0.18.2] - 2026-02-04
### Added
- Add user login with username and password on the package.

### Changed
- No changes.

### Removed
- Remove debug prints


## [0.16.0] - 2025-02-25
### Added
- Creation of class `StreamlitDataFrameState`. It helps to set and adjust
  dataframe types according to state class configuration. Possibly in the
  future, some data validation class cloud be used.

### Changed
- No changes.

### Removed
- Remove debug prints

## [0.15.3] - 2025-02-18

### Added

- No adds.

### Changed

- No changes.

### Removed

- Remove debug prints

## [0.15.2] - 2025-02-18

### Added

- Add state debug when `DEBUG_FILES_PATH` is set.

### Changed

- No changes.

### Removed

- Remove debug prints


## [0.15.1] - 2025-02-18

### Added

- No adds.

### Changed

- Adjusts on doc strings.

### Removed

- Remove debug prints
