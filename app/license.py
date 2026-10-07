"""License management for Higgfield MCP.

Provides license activation and validation utilities.
"""

from app.core.license_server import LicenseWatcher, check_license, license_watcher


__all__ = ["LicenseWatcher", "check_license", "license_watcher"]