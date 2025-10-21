"""Decorator for Uptime Robot"""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from typing import TYPE_CHECKING

import aiohttp

from pyuptimerobot import exceptions

from .const import API_BASE_URL, API_HEADERS, LOGGER
from .models import UptimeRobotApiResponse

if TYPE_CHECKING:
    from .uptimerobot import UptimeRobot


def api_request(api_path: str, method: str = "GET"):
    """Decorator for Uptime Robot API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client: UptimeRobot = args[0]
            url = f"{API_BASE_URL}{api_path}"
            if "monitor_id" in kwargs:
                url = url.format(monitor_id=kwargs.pop("monitor_id"))
            headers = {
                "Authorization": f"Bearer {client._api_key}",
                **API_HEADERS,
            }
            LOGGER.debug("Requesting %s with payload %s", url, kwargs)
            try:
                request = await client._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=kwargs,
                    timeout=aiohttp.ClientTimeout(total=10),
                )

                if request.status != HTTPStatus.OK:
                    if request.status == HTTPStatus.UNAUTHORIZED:
                        raise exceptions.UptimeRobotAuthenticationException(
                            f"Authentication failed for '{url}' with status code '{request.status}'"
                        )
                    raise exceptions.UptimeRobotConnectionException(
                        f"Request for '{url}' failed with status code '{request.status}'"
                    )

                result = await request.json()
            except aiohttp.ClientError as exception:
                raise exceptions.UptimeRobotConnectionException(
                    f"Request exception for '{url}' with - {exception}"
                ) from exception

            except asyncio.TimeoutError:
                raise exceptions.UptimeRobotConnectionException(
                    f"Request timeout for '{url}'"
                ) from None

            except exceptions.UptimeRobotConnectionException as exception:
                raise exceptions.UptimeRobotConnectionException(
                    exception
                ) from exception

            except exceptions.UptimeRobotAuthenticationException as exception:
                raise exceptions.UptimeRobotAuthenticationException(
                    exception
                ) from exception

            except exceptions.UptimeRobotException as exception:
                raise exceptions.UptimeRobotException(exception) from exception

            except (Exception, BaseException) as exception:
                raise exceptions.UptimeRobotException(
                    f"Unexpected exception for '{url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", url, result)

            return UptimeRobotApiResponse.from_dict(
                {**result, "_api_path": api_path, "_method": method}
            )

        return wrapper

    return decorator
