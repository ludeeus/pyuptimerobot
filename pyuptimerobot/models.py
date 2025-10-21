"""Uptime Robot models"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


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
    monitorsCount: int = 0

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
    friendlyName: str = ""
    url: str = ""
    type: str = ""
    interval: int = 0
    status: str = ""

    @staticmethod
    def from_dict(data: dict[str, Any]) -> UptimeRobotMonitor:
        """Generate object from json."""
        obj: dict[str, Any] = {}
        for key, value in data.items():
            if hasattr(UptimeRobotMonitor, key):
                obj[key] = value

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
        obj: dict[str, Any] = {"status": APIStatus(data.get("stat", "ok"))}
        if obj["status"] == APIStatus.FAIL:
            obj["error"] = UptimeRobotApiError.from_dict(data["error"])
        else:
            for key, value in data.items():
                if hasattr(UptimeRobotApiResponse, key):
                    obj[key] = value

            if "pagination" in data:
                obj["pagination"] = UptimeRobotPagination.from_dict(data["pagination"])

            if data["_api_path"].endswith("/monitors"):
                obj["data"] = [
                    UptimeRobotMonitor.from_dict(monitor) for monitor in data["data"]
                ]
            else:
                obj["data"] = UptimeRobotAccount.from_dict(data)

        return UptimeRobotApiResponse(**obj)
