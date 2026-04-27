"""Decorator for Uptime Robot"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, TypeVar, cast

import aiohttp

from pyuptimerobot import exceptions

from .const import (
    API_BASE_URL,
    API_PATH_MONITOR_DETAIL,
    API_STATUS_TO_ACTION,
    LOGGER,
)
from .models import UptimeRobotApiResponse

if TYPE_CHECKING:
    from .uptimerobot import UptimeRobot


ResponseDataT = TypeVar("ResponseDataT")


def api_request(
    api_path: str, method: str = "GET"
) -> Callable[
    [Callable[..., Coroutine[Any, Any, UptimeRobotApiResponse[ResponseDataT]]]],
    Callable[..., Coroutine[Any, Any, UptimeRobotApiResponse[ResponseDataT]]],
]:
    """Decorator for Uptime Robot API request"""

    def decorator(
        _func: Callable[..., Coroutine[Any, Any, UptimeRobotApiResponse[ResponseDataT]]],
    ) -> Callable[..., Coroutine[Any, Any, UptimeRobotApiResponse[ResponseDataT]]]:
        """Decorator"""

        async def wrapper(*args: Any, **kwargs: Any) -> UptimeRobotApiResponse[ResponseDataT]:
            """Wrapper"""
            client = cast("UptimeRobot", args[0])
            url = f"{API_BASE_URL}{api_path}"
            if (monitor_id := kwargs.pop("monitor_id", None)) is not None:
                url = url.format(monitor_id=monitor_id)
            if (
                api_path == API_PATH_MONITOR_DETAIL
                and (status := kwargs.get("status")) is not None
                and (action := API_STATUS_TO_ACTION.get(status)) is not None
            ):
                url = f"{url}/{action}"

            LOGGER.debug("Requesting %s with payload %s", url, kwargs)
            try:
                request = await client._session.request(
                    method=method,
                    url=url,
                    headers={
                        "Authorization": f"Bearer {client._api_key}",
                        "Content-Type": "application/json",
                    },
                    json=kwargs,
                    timeout=aiohttp.ClientTimeout(total=10),
                )

                if request.status not in (
                    HTTPStatus.OK,
                    HTTPStatus.CREATED,
                ):
                    if request.status == HTTPStatus.UNAUTHORIZED:
                        raise exceptions.UptimeRobotAuthenticationException(
                            f"Authentication failed for '{url}'"
                            f" with status code '{request.status}'"
                        )
                    raise exceptions.UptimeRobotConnectionException(
                        f"Request for '{url}' failed with status code '{request.status}'"
                    )

                result = await request.json()
            except aiohttp.ClientError as exception:
                raise exceptions.UptimeRobotConnectionException(
                    f"Request exception for '{url}' with - {exception}"
                ) from exception

            except TimeoutError:
                raise exceptions.UptimeRobotConnectionException(
                    f"Request timeout for '{url}'"
                ) from None

            except exceptions.UptimeRobotException:
                raise

            except Exception as exception:
                raise exceptions.UptimeRobotException(
                    f"Unexpected exception for '{url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", url, result)

            return UptimeRobotApiResponse.from_dict(
                {**result, "_api_path": api_path, "_method": method}
            )

        return wrapper

    return decorator
