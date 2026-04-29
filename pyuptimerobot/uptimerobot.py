"""Uptime Robot client."""

from typing import Any

from aiohttp import ClientSession

from .const import (
    API_PATH_MONITOR_DETAIL,
    API_PATH_MONITORS,
    API_PATH_USER_ME,
)
from .decorator import api_request
from .models import UptimeRobotAccount, UptimeRobotApiResponse, UptimeRobotMonitor


class UptimeRobot:
    """This class is used to get information from Uptime Robot."""

    def __init__(self, api_key: str, session: ClientSession) -> None:
        """Initialize"""
        self._api_key: str = api_key
        self._session: ClientSession = session

    @api_request(API_PATH_MONITORS)
    async def async_get_monitors(  # type: ignore[empty-body]
        self, **kwargs: Any
    ) -> UptimeRobotApiResponse[list[UptimeRobotMonitor]]:
        """Get monitors from API."""

    @api_request(API_PATH_USER_ME)
    async def async_get_account_details(  # type: ignore[empty-body]
        self, **kwargs: Any
    ) -> UptimeRobotApiResponse[UptimeRobotAccount]:
        """Get account details from API."""

    @api_request(API_PATH_MONITOR_DETAIL, method="PATCH")
    async def async_edit_monitor(  # type: ignore[empty-body]
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Edit monitor settings via API."""

    @api_request("/monitors/{monitor_id}/pause", method="POST")
    async def async_pause_monitor(  # type: ignore[empty-body]
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Pause a monitor via API."""

    @api_request("/monitors/{monitor_id}/start", method="POST")
    async def async_start_monitor(  # type: ignore[empty-body]
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Start a monitor via API."""

    @api_request("/monitors/{monitor_id}/reset", method="POST")
    async def async_reset_monitor(  # type: ignore[empty-body]
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Reset a monitor via API."""
