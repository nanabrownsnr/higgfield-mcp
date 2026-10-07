# Higgfield MCP

A production-ready MCP (Model Context Protocol) server for API key management, generation tracking, and external API calling with Twynity integration.

## Features

- ✅ **JWT Authentication** - Secure bearer token verification with account-service JWKS
- ✅ **Persona-Based Access** - Strict `(user_id, persona_id)` pairing for multi-tenancy
- ✅ **Encrypted Storage** - Fernet encryption for sensitive credentials
- ✅ **MCP Tools Integration** - Tools accessible to both LLMs and MCP Apps UI
- ✅ **External API Calls** - Call third-party services using stored credentials
- ✅ **File Operations** - Local file system access for owners
- ✅ **Usage Tracking** - Fire-and-forget usage reporting
- ✅ **License Management** - Automatic license validation with grace period
- ✅ **React UI** - Built-in MCP Apps UI for tool visualization
- ✅ **Comprehensive Testing** - Unit and integration tests
- ✅ **Docker Support** - Multi-stage Docker builds

## Quick Start

### Prerequisites

- Python 3.12+
- npm (for UI development)
- Docker (optional, but recommended)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd higgfield-mcp
```

2. Install dependencies:
```bash
uv sync
```

3. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your settings (see Configuration section).

4. Run the server:
```bash
uv run python -m uvicorn app.main:app --reload
```

5. Access the API docs:
```
http://localhost:8000/docs
```

## Configuration

Required environment variables:

```env
# Service Identity
SERVICE_ID=higgfield-mcp
APP_TITLE=Higgfield MCP
APP_VERSION=1.0.0

# Security
ALLOWED_ORIGINS=*
PERSONA_ID_HEADER=Persona-Id

# Account Service (JWT verification)
ACCOUNT_SERVICE_URL=http://account_service:8000
ACCOUNT_SERVICE_JWKS_ENDPOINT=/.well-known/jwks.json

# MongoDB
MONGODB_URI=mongodb://mongo:27017
MONGODB_DB=higgfield
ENCRYPTION_KEY=REPLACE_WITH_32_CHAR_KEY_FOR_FERNET

# Usage Reporting (optional)
USAGE_REPORT_ENDPOINT=http://usage-reporting:8000/api/v1/usage
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_auth.py

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

### Linting

```bash
# Check code style
uv run ruff check app tests

# Fix auto-fixable issues
uv run ruff check --fix app tests
```

### Building UI

```bash
cd app/ui/file_dir
npm install
npm run build
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Build Docker image
docker build -t higgfield-mcp .
```

## Architecture

### Core Components

- **`app/auth.py`**: JWT verification and identity resolution
- **`app/config.py`**: Service configuration and settings
- **`app/connection_store.py`**: Encrypted MongoDB storage
- **`app/license.py`**: License management
- **`app/usage.py`**: Usage tracking middleware
- **`app/twynity.py`**: Twynity-specific HTTP routes

### MCP Tools

- **`app/tools/api_call.py`**: External API calls
- **`app/tools/files.py`**: File system operations
- **`app/tools/generational.py`**: Generation tracking
- **`app/tools/render_content.py`**: Content rendering

### API Endpoints

- **`GET /api/v1/manifest/mcp.json`**: Public manifest endpoint
- **`GET /api/v1/schema`**: Configuration schema
- **`POST /api/v1/keys`**: Create API key
- **`GET /api/v1/keys`**: List API keys
- **`POST /api/v1/generations`**: Create generation
- **`GET /api/v1/generations`**: List generations

### Twynity Integration

- Custom HTTP routes with explicit JWT verification
- MCP Apps UI support with tool-to-resource linking
- Persona-Id header forwarding for authenticated calls
- External connections manifest

## Security Best Practices

1. **Never disable signature verification** - Always use JWT with JWKS
2. **Enforce exact `(user_id, persona_id)` pairing** - Never fall back to user-only lookups
3. **Encrypt all credentials** - Use Fernet encryption before storage
4. **Never log or return secrets** - Use safe metadata-only GET responses
5. **Validate Persona-Id from headers** - Never accept from untrusted sources
6. **Use timeouts on outbound calls** - Prevent hanging requests

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `uv run pytest`
5. Run linter: `uv run ruff check app tests`
6. Submit a pull request

## Support

For issues and questions, please open an issue on GitHub or contact the development team.

## Version History

- **1.0.0** - Initial release with basic MCP functionality
- **1.0.1** - Added Twynity integration and comprehensive testing

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version-specific changes.