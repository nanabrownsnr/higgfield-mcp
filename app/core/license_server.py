"""License server integration and validation for Higgfield MCP.

Provides license watching and validation with grace period support.
"""

import asyncio
import uuid
from datetime import datetime, timedelta

from app.config import settings
from app.core.connection_store import get_connection_store


class LicenseWatcher:
    """Background task for license validation."""

    def __init__(self) -> None:
        """Initialize license watcher."""
        self._task: Optional[asyncio.Task] = None
        self._last_check: Optional[datetime] = None
        self._failures: int = 0
        self._grace_period: int = 14  # 14 days grace period

    async def check_license(self) -> dict[str, Any]:
        """Check current license status.

        Returns:
            Dictionary with status and optionally error message
        """
        if settings.LICENSE_KEY == "REPLACE_WITH_KEY":
            # If no license key configured, assume valid for development
            return {
                "valid": True,
                "mode": "development",
            }

        # In production, validate against license server
        try:
            from jose import jwt

            device_id = self._get_device_id()
            token = settings.LICENSE_KEY

            payload = jwt.decode(
                token,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )

            if payload.get("service_id") != settings.SERVICE_ID:
                return {"valid": False, "error": "Service ID mismatch"}

            if payload.get("device_id") != device_id:
                return {"valid": False, "error": "Device ID mismatch"}

            return {"valid": True, "expires_at": payload.get("expires_at")}

        except Exception as e:
            self._failures += 1
            if self._failures > self._grace_period:
                return {"valid": False, "error": f"License validation failed: {str(e)}"}

            return {
                "valid": True,
                "error": str(e),
                "mode": "grace_period",
            }

    def _get_device_id(self) -> str:
        """Generate persistent device ID based on MAC address."""
        # Get MAC address as device fingerprint
        mac_address = uuid.getnode()
        return str(mac_address)

    async def _run(self) -> None:
        """Run continuous license checks."""
        while True:
            try:
                await self.check_license()
                self._failures = 0
            except Exception:
                pass

            # Check every 24 hours
            await asyncio.sleep(86400)

    async def start(self) -> None:
        """Start the license watcher task."""
        if self._task is None:
            self._task = asyncio.create_task(self._run())


license_watcher = LicenseWatcher()


async def check_license() -> dict[str, Any]:
    """Convenience function to check license status."""
    return await license_watcher.check_license()