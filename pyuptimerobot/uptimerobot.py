"""Uptime Robot client."""

from collections.abc import Callable
from email.utils import parsedate_to_datetime
from http import HTTPStatus
from time import time
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
    UptimeRobotRateLimitException,
)
from .models import (
    RDT,
    UptimeRobotAccount,
    UptimeRobotApiResponse,
    UptimeRobotMonitor,
    UptimeRobotRateLimit,
)


def _parse_int(value: str | None) -> int | None:
    """Parse a string to int, returning None if missing or invalid."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError, TypeError:
        return None


def _parse_reset(value: str | None) -> int | None:
    """Parse the X-RateLimit-Reset header to seconds until the rate limit resets.

    The value is assumed to be a delta in seconds, but values above 1000
    that represent an epoch timestamp in the future are converted to a delta.
    """
    if (parsed := _parse_int(value)) is None:
        return None
    now = time()
    if parsed > 1000 and parsed > now:
        return int(parsed - now)
    return parsed


def _parse_retry_after(value: str | None) -> int | None:
    """Parse the Retry-After header to seconds, handling both delta and HTTP-date forms."""
    if value is None:
        return None
    if (parsed := _parse_int(value)) is not None:
        return parsed
    try:
        retry_at = parsedate_to_datetime(value)
    except ValueError, TypeError:
        return None
    return max(0, int(retry_at.timestamp() - time()))


class UptimeRobot:
    """This class is used to get information from Uptime Robot."""

    def __init__(self, api_key: str, session: ClientSession) -> None:
        """Initialize"""
        self._api_key: str = api_key
        self._session: ClientSession = session
        self._ratelimit: UptimeRobotRateLimit | None = None

    @property
    def ratelimit(self) -> UptimeRobotRateLimit | None:
        """Rate limit information from the most recent response."""
        return self._ratelimit

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
            async with self._session.request(
                method=method,
                url=url,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json=json,
                timeout=ClientTimeout(total=10),
            ) as request:
                self._ratelimit = ratelimit = UptimeRobotRateLimit(
                    limit=_parse_int(request.headers.get("X-RateLimit-Limit")),
                    remaining=_parse_int(request.headers.get("X-RateLimit-Remaining")),
                    reset=_parse_reset(request.headers.get("X-RateLimit-Reset")),
                    retry_after=_parse_retry_after(request.headers.get("Retry-After")),
                    updated_at=time(),
                )

                if request.status in EXPECTED_API_STATUS_CODES:
                    result = await request.json()
                    LOGGER.debug(
                        "Requesting %s returned %s (ratelimit %s/%s)",
                        url,
                        result,
                        ratelimit.get("remaining"),
                        ratelimit.get("limit"),
                    )
                    return UptimeRobotApiResponse.from_dict(
                        data=data_transformer(result),
                        api_path=api_path,
                        method=method,
                        pagination=result.get("pagination"),
                        ratelimit=ratelimit,
                    )

                if request.status == HTTPStatus.TOO_MANY_REQUESTS:
                    raise UptimeRobotRateLimitException(
                        f"Rate limit exceeded for '{url}'", ratelimit=ratelimit
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
