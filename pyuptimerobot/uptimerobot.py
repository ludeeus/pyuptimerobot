"""Uptime Robot client."""

from aiohttp import ClientSession

from .decorator import api_request
from .models import UptimeRobotApiResponse


class UptimeRobot:
    """This class is used to get information from Uptime Robot."""

    def __init__(self, api_key: str, session: ClientSession) -> None:
        """Initialize"""
        self._api_key: str = api_key
        self._session: ClientSession = session

    @api_request("/monitors")
    async def async_get_monitors(  # type: ignore[empty-body]
        self, **kwargs
    ) -> UptimeRobotApiResponse:
        """Get monitors from API."""

    @api_request("/user/me")
    async def async_get_account_details(self, **kwargs) -> UptimeRobotApiResponse:  # type: ignore[empty-body]
        """Get account details from API."""

    @api_request("/monitors/{monitor_id}", method="PATCH")
    async def async_edit_monitor(  # type: ignore[empty-body]
        self,
        monitor_id: int,
        **kwargs,
    ) -> UptimeRobotApiResponse:
        """Edit monitor settings via API."""
