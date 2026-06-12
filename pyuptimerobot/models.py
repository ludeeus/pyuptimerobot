"""Uptime Robot models"""

from __future__ import annotations

from annotationlib import get_annotations
from dataclasses import dataclass
from typing import Any, Generic, TypedDict, TypeVar

T = TypeVar("T", bound="UptimeRobotBaseModel")
RDT = TypeVar("RDT")


@dataclass
class UptimeRobotBaseModel:
    """UptimeRobotBaseModel."""

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        classkeys = get_annotations(cls).keys()
        for key, value in data.items():
            if key in classkeys:
                obj[key] = value

        return cls(**obj)


@dataclass
class UptimeRobotPagination(UptimeRobotBaseModel):
    """Pagination model for Uptime Robot."""

    offset: int = 0
    limit: int = 0
    total: int = 0


@dataclass
class UptimeRobotAccount(UptimeRobotBaseModel):
    """Account model for Uptime Robot."""

    email: str
    monitorsCount: int


@dataclass
class UptimeRobotMonitor(UptimeRobotBaseModel):
    """Monitor model for Uptime Robot."""

    id: int
    friendlyName: str
    interval: int
    url: str
    status: str | None = None
    type: str | None = None


class UptimeRobotRateLimit(TypedDict):
    """Rate limit information from API response headers.

    Attributes:
        limit: The current rate limit (number of calls allowed in the current period).
        remaining: The number of calls left in the current period.
        reset: The time in seconds until the rate limit resets.
            Epoch timestamps sent by the server are converted to a delta.
        retry_after: The number of seconds after which you should retry the call.
        updated_at: A Unix timestamp when the rate limit info was captured.
    """

    limit: int | None
    remaining: int | None
    reset: int | None
    retry_after: int | None
    updated_at: float


@dataclass
class UptimeRobotApiResponse(Generic[RDT]):
    """API response model for Uptime Robot."""

    _method: str
    _api_path: str

    data: RDT
    pagination: UptimeRobotPagination | None = None
    ratelimit: UptimeRobotRateLimit | None = None

    @classmethod
    def from_dict(
        cls: type[UptimeRobotApiResponse[RDT]],
        data: RDT,
        api_path: str,
        method: str,
        pagination: dict[str, Any] | None = None,
        ratelimit: UptimeRobotRateLimit | None = None,
    ) -> UptimeRobotApiResponse[RDT]:
        """Generate a common API response object."""
        return UptimeRobotApiResponse(
            _api_path=api_path,
            _method=method,
            data=data,
            pagination=(UptimeRobotPagination.from_dict(pagination) if pagination else None),
            ratelimit=ratelimit,
        )
