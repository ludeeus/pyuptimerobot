"""Uptime Robot exceptions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import UptimeRobotRateLimit


class UptimeRobotException(Exception):
    """Base Uptime Robot exception."""


class UptimeRobotConnectionException(UptimeRobotException):
    """Uptime Robot connection exception."""


class UptimeRobotAuthenticationException(UptimeRobotException):
    """Uptime Robot authentication exception."""


class UptimeRobotRateLimitException(UptimeRobotConnectionException):
    """Uptime Robot rate limit exception."""

    def __init__(self, *args: object, ratelimit: UptimeRobotRateLimit) -> None:
        """Initialize."""
        super().__init__(*args)
        self._ratelimit = ratelimit

    @property
    def limit(self) -> int | None:
        """The current rate limit (number of calls allowed in the current period)."""
        return self._ratelimit.get("limit")

    @property
    def remaining(self) -> int | None:
        """The number of calls left in the current period."""
        return self._ratelimit.get("remaining")

    @property
    def reset(self) -> int | None:
        """The time in seconds until the rate limit resets."""
        return self._ratelimit.get("reset")

    @property
    def retry_after(self) -> int | None:
        """The number of seconds after which you should retry the call."""
        return self._ratelimit.get("retry_after")

    @property
    def updated_at(self) -> float:
        """A Unix timestamp when the rate limit info was captured."""
        return self._ratelimit["updated_at"]
