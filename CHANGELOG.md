# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-05-24

### Changed
- Renamed PyPI distribution to `publicip-cli` to avoid similarity conflict with existing `public-ip` package
- CLI command, Python module, and all functionality remain unchanged

### Fixed
- Corrected provider URLs for ident.me (`4.ident.me`) and seeip (`ipv4.seeip.org`)

## [0.1.0] - 2026-05-24

### Added
- Initial release
- Automatic public IP detection with fallback across four providers (ipify, icanhazip, ident.me, seeip)
- `--provider` flag to force a specific provider
- `--all` flag to query all providers
- `--format plain|json` output modes
- `--verbose` flag to include provider name in output
