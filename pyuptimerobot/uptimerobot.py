"""Uptime Robot client."""

from collections.abc import Callable
from http import HTTPStatus
from typing import Any

from aiohttp import ClientError, ClientSession, ClientTimeout

from .const import (
    API_BASE_URL,
    EXPECTED_API_STATUS_CODES,
    LOGGER,
)
from .exceptions import (
    UptimeRobotAuthenticationException,
    UptimeRobotConnectionException,
    UptimeRobotException,
)
from .models import RDT, UptimeRobotAccount, UptimeRobotApiResponse, UptimeRobotMonitor


class UptimeRobot:
    """This class is used to get information from Uptime Robot."""

    def __init__(self, api_key: str, session: ClientSession) -> None:
        """Initialize"""
        self._api_key: str = api_key
        self._session: ClientSession = session

    async def _call_api(
        self,
        *,
        api_path: str,
        data_transformer: Callable[[dict[str, Any]], RDT],
        method: str = "GET",
        json: Any = None,
    ) -> UptimeRobotApiResponse[RDT]:
        """Call the API."""
        url = f"{API_BASE_URL}{api_path}"
        LOGGER.debug("Requesting %s with payload %s", url, json)
        try:
            request = await self._session.request(
                method=method,
                url=url,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=json,
                timeout=ClientTimeout(total=10),
            )

            if request.status in EXPECTED_API_STATUS_CODES:
                result = await request.json()
                LOGGER.debug("Requesting %s returned %s", url, result)
                return UptimeRobotApiResponse.from_dict(
                    data=data_transformer(result),
                    api_path=api_path,
                    method=method,
                    pagination=result.get("pagination"),
                )

            if request.status == HTTPStatus.UNAUTHORIZED:
                raise UptimeRobotAuthenticationException(
                    f"Authentication failed for '{url}' with status code '{request.status}'"
                )
            raise UptimeRobotConnectionException(
                f"Request for '{url}' failed with status code '{request.status}'"
            )

        except ClientError as exception:
            raise UptimeRobotConnectionException(
                f"Request exception for '{url}' with - {exception}"
            ) from exception

        except TimeoutError:
            raise UptimeRobotConnectionException(f"Request timeout for '{url}'") from None

        except UptimeRobotException:
            raise

        except Exception as exception:
            raise UptimeRobotException(
                f"Unexpected exception for '{url}' with - {exception}"
            ) from exception

    async def async_get_monitors(
        self, **kwargs: Any
    ) -> UptimeRobotApiResponse[list[UptimeRobotMonitor]]:
        """Get monitors from API."""

        return await self._call_api(
            api_path="/monitors",
            json=kwargs,
            data_transformer=lambda x: [
                UptimeRobotMonitor.from_dict(monitor) for monitor in x.get("data", [])
            ],
        )

    async def async_get_account_details(
        self, **kwargs: Any
    ) -> UptimeRobotApiResponse[UptimeRobotAccount]:
        """Get account details from API."""
        return await self._call_api(
            api_path="/user/me", json=kwargs, data_transformer=UptimeRobotAccount.from_dict
        )

    async def async_edit_monitor(
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Edit monitor settings via API."""
        return await self._call_api(
            api_path=f"/monitors/{monitor_id}",
            method="PATCH",
            json=kwargs,
            data_transformer=UptimeRobotMonitor.from_dict,
        )

    async def async_pause_monitor(
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Pause a monitor via API."""
        return await self._call_api(
            api_path=f"/monitors/{monitor_id}/pause",
            method="POST",
            json=kwargs,
            data_transformer=UptimeRobotMonitor.from_dict,
        )

    async def async_start_monitor(
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Start a monitor via API."""
        return await self._call_api(
            api_path=f"/monitors/{monitor_id}/start",
            method="POST",
            json=kwargs,
            data_transformer=UptimeRobotMonitor.from_dict,
        )

    async def async_reset_monitor(
        self,
        *,
        monitor_id: int,
        **kwargs: Any,
    ) -> UptimeRobotApiResponse[UptimeRobotMonitor]:
        """Reset a monitor via API."""
        return await self._call_api(
            api_path=f"/monitors/{monitor_id}/reset",
            method="POST",
            json=kwargs,
            data_transformer=UptimeRobotMonitor.from_dict,
        )
