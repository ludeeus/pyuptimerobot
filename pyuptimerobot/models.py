"""Uptime Robot models"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class MonitorType(Enum):
    """Monitors type."""

    HTTP = 1
    keyword = 2
    ping = 3
    port = 4
    heartbeat = 5


class APIStatus(str, Enum):
    """API status."""

    OK = "ok"
    FAIL = "fail"


class UptimeRobotBaseModel:
    """UptimeRobotBaseModel."""


@dataclass
class UptimeRobotPagination(UptimeRobotBaseModel):
    """Pagination model for Uptime Robot."""

    offset: int = 0
    limit: int = 0
    total: int = 0

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotPagination:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeRobotPagination, key):
                obj[key] = value

        return UptimeRobotPagination(**obj)


@dataclass
class UptimeRobotApiError(UptimeRobotBaseModel):
    """API error model for Uptime Robot."""

    type: str = ""
    parameter_name: str = ""
    message: str = ""
    passed_value: str = ""

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotApiError:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeRobotApiError, key):
                obj[key] = value

        return UptimeRobotApiError(**obj)


@dataclass
class UptimeRobotAccount(UptimeRobotBaseModel):
    """Account model for Uptime Robot."""

    email: str = ""
    user_id: int = 0
    up_monitors: int = 0
    down_monitors: int = 0
    paused_monitors: int = 0

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotAccount:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeRobotAccount, key):
                obj[key] = value

        return UptimeRobotAccount(**obj)


@dataclass
class UptimeRobotMonitor(UptimeRobotBaseModel):
    """Monitor model for Uptime Robot."""

    id: int = 0
    friendly_name: str = ""
    url: str = ""
    type: MonitorType = MonitorType.HTTP
    interval: int = 0
    status: int = 0

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotMonitor:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeRobotMonitor, key):
                obj[key] = value

        if obj.get("type"):
            obj["type"] = MonitorType(obj["type"])

        return UptimeRobotMonitor(**obj)


@dataclass
class UptimeRobotApiResponse(UptimeRobotBaseModel):
    """API response model for Uptime Robot."""

    _method: str | None = None
    _api_path: str | None = None
    status: APIStatus = APIStatus.FAIL
    error: UptimeRobotApiError | None = None
    data: list[UptimeRobotMonitor] | UptimeRobotAccount | None = None
    pagination: dict[str, Any] | None = None

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotApiResponse:
        """Generate object from json."""
        obj: dict[str, Any] = {"status": APIStatus(data["stat"])}
        if obj["status"] == APIStatus.FAIL:
            obj["error"] = UptimeRobotApiError.from_dict(data["error"])
        else:
            for key, value in data.items():
                if hasattr(UptimeRobotApiResponse, key):
                    obj[key] = value

            if "pagination" in data:
                obj["pagination"] = UptimeRobotPagination.from_dict(data["pagination"])

            if "monitors" in data:
                obj["data"] = [
                    UptimeRobotMonitor.from_dict(monitor)
                    for monitor in data["monitors"]
                ]
            if "account" in data:
                obj["data"] = UptimeRobotAccount.from_dict(data["account"])

        return UptimeRobotApiResponse(**obj)
