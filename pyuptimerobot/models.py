"""Uptime Robot models"""

from __future__ import annotations

from annotationlib import get_annotations
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

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


@dataclass
class UptimeRobotApiResponse(Generic[RDT]):
    """API response model for Uptime Robot."""

    _method: str
    _api_path: str

    data: RDT
    pagination: UptimeRobotPagination | None = None

    @classmethod
    def from_dict(
        cls: type[UptimeRobotApiResponse[RDT]],
        data: RDT,
        api_path: str,
        method: str,
        pagination: dict[str, Any] | None = None,
    ) -> UptimeRobotApiResponse[RDT]:
        """Generate a common API response object."""
        return UptimeRobotApiResponse(
            _api_path=api_path,
            _method=method,
            data=data,
            pagination=(UptimeRobotPagination.from_dict(pagination) if pagination else None),
        )
