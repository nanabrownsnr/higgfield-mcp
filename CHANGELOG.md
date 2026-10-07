# Changelog

All notable changes to Higgfield MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-10-07

### Added
- Updated dependencies to match Twynity template
- Added proper JWT verification with JWKS endpoint
- Implemented Twynity-specific HTTP routes with authentication
- Added usage tracking middleware with fire-and-forget reporting
- Created comprehensive test suite
- Added license management with grace period
- Implemented encrypted MongoDB storage
- Created .env.example for easy configuration
- Added documentation and README
- Added AGENTS.md developer guide

### Changed
- Improved authentication security (removed signature verification bypass)
- Updated pyproject.toml with dev dependencies
- Enhanced configuration with more environment variables
- Improved error handling across all modules

### Fixed
- Fixed JWT verification in auth module
- Fixed file operations to use proper tool contracts
- Fixed missing Persona-Id header validation
- Fixed missing manifest and schema endpoints

## [1.0.0] - 2026-10-06

### Added
- Initial release of Higgfield MCP
- Basic MCP tools for API calls and file operations
- API endpoints for key and generation management
- React UI for file directory browsing
- Docker support with multi-stage builds
- MongoDB storage with async operations
- JWT-based authentication

### Changed
- N/A (first release)