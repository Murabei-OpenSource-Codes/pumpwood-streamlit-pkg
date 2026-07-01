# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Migrate build from ``setup.py`` to Poetry (``pyproject_template.toml``).
- Update README, module docstrings, and build script.

## [0.18.12] - 2026-05-06

### Added

- Add ``URLParams`` class in ``query_params.py`` to facilitate
  management of URL parameters with URL-safe base64/JSON encoding.
- Add ``URL_PARAMS`` attribute to ``URLParams`` for declarative
  configuration of query params.
- Add ``has_url_params()`` method to check if all required URL params
  are present.
- Add ``get_url_params()`` method to retrieve raw URL param values.
- Add ``render_filters_section()`` method to conditionally render the
  filter grid based on the presence of valid URL params.
- Add ``encode_url_params()`` and ``decode_url_params()`` utility
  methods for base64/JSON conversion.

## [0.18.7] - 2026-02-02

### Added

- Add ``PumpwoodStreamlitRegister`` to register dashboard service and
  route at Kong.

### Removed

- Remove debug prints.

## [0.18.2] - 2026-02-04

### Added

- Add user login with username and password via
  ``StreamlitUserAuthentication``.

### Removed

- Remove debug prints.

## [0.16.0] - 2025-02-25

### Added

- Add ``StreamlitDataFrameState`` to set and adjust dataframe types
  according to state class configuration.

### Removed

- Remove debug prints.

## [0.15.3] - 2025-02-18

### Removed

- Remove debug prints.

## [0.15.2] - 2025-02-18

### Added

- Add state debug when ``DEBUG_FILES_PATH`` is set.

### Removed

- Remove debug prints.

## [0.15.1] - 2025-02-18

### Changed

- Adjust docstrings.

### Removed

- Remove debug prints.
