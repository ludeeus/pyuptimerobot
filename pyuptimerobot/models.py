"""Uptime Robot models"""

from __future__ import annotations

from annotationlib import get_annotations
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast

from .const import API_PATH_MONITOR_DETAIL, API_PATH_MONITORS, API_PATH_USER_ME

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
class UptimeRobotApiResponse(UptimeRobotBaseModel, Generic[RDT]):
    """API response model for Uptime Robot."""

    _method: str
    _api_path: str

    data: RDT
    pagination: UptimeRobotPagination | None = None

    @classmethod
    def from_dict(
        cls: type[UptimeRobotApiResponse[RDT]], data: dict[str, Any]
    ) -> UptimeRobotApiResponse[RDT]:
        """Generate object from json."""
        apipath = data.pop("_api_path")
        method = data.pop("_method")
        pagination = data.pop("pagination", None)

        def _convert_data(raw_data: dict[str, Any]) -> RDT:
            """Convert raw API data to appropriate model type based on endpoint."""
            if apipath == API_PATH_MONITORS:
                return cast(
                    RDT,
                    [
                        UptimeRobotMonitor.from_dict(monitor)
                        for monitor in raw_data["data"]
                    ],
                )
            elif apipath == API_PATH_MONITOR_DETAIL:
                return cast(RDT, UptimeRobotMonitor.from_dict(raw_data))
            elif apipath == API_PATH_USER_ME:
                return cast(RDT, UptimeRobotAccount.from_dict(raw_data))
            else:
                # Fallback for unknown endpoints - return raw data
                return cast(RDT, raw_data)

        return UptimeRobotApiResponse(
            _api_path=apipath,
            _method=method,
            data=_convert_data(data),
            pagination=(
                UptimeRobotPagination.from_dict(pagination) if pagination else None
            ),
        )
