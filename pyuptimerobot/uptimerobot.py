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

    @api_request("/getMonitors")
    async def async_get_monitors(self, **kwargs) -> UptimeRobotApiResponse:
        """Get monitors from API."""

    @api_request("/getAccountDetails")
    async def async_get_account_details(self, **kwargs) -> UptimeRobotApiResponse:
        """Get account details from API."""
