# Changelog

This file contains the changes made between released versions.

The format is based on [Keep a changelog](https://keepachangelog.com/) and the versioning tries to follow
[Semantic Versioning](https://semver.org).

## 2.1.0
### Added
- SHA256 checksum of a document is stored on the side, too
- Duplicates are detected and skipped when adding/picking up new documents
- `keep-name` configuration option per cabinet


## 2.0.1
### Fixed
- Fixed issues with `last_modified` and the new unified timestamp format


## 2.0.0
### Changed
- Big refactoring to use metaindex as the backend for quick searching
- Simplified the file structure for the storage

