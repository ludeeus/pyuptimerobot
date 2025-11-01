"""Uptime Robot client."""

from aiohttp import ClientSession

from .const import API_PATH_MONITOR_DETAIL, API_PATH_MONITORS, API_PATH_USER_ME
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
        self, **kwargs
    ) -> UptimeRobotApiResponse[list[UptimeRobotMonitor]]:
        """Get monitors from API."""

    @api_request(API_PATH_USER_ME)
    async def async_get_account_details(self, **kwargs) -> UptimeRobotApiResponse[UptimeRobotAccount]:  # type: ignore[empty-body]
        """Get account details from API."""

    @api_request(API_PATH_MONITOR_DETAIL, method="PATCH")
    async def async_edit_monitor(  # type: ignore[empty-body]
        self,
        monitor_id: int,
        **kwargs,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Edit monitor settings via API."""
