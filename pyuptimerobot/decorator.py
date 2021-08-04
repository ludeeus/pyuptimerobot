"""Decorator for Uptime Robot"""
from __future__ import annotations

import asyncio

import aiohttp
import async_timeout

from pyuptimerobot.exceptions import (
    UptimeRobotConnectionException,
    UptimeRobotException,
)

from .const import API_BASE_URL, API_HEADERS, LOGGER
from .models import UptimeRobotApiResponse


def api_request(api_path: str, method: str = "POST"):
    """Decorator for Uptime Robot API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client = args[0]
            request_data = f"api_key={client._api_key}&format=json"
            url = f"{API_BASE_URL}{api_path}"
            if kwargs:
                for key, value in kwargs.items():
                    request_data += f"&{key}={value}"
            LOGGER.debug("Requesting %s", url)
            try:
                async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                    request = await client._session.request(
                        method=method,
                        url=url,
                        headers=API_HEADERS,
                        data=request_data,
                    )

                    if request.status != 200:
                        raise UptimeRobotConnectionException(
                            f"Request for '{url}' failed with status code '{request.status}'"
                        )

                result = await request.json()
            except aiohttp.ClientError as exception:
                raise UptimeRobotConnectionException(
                    f"Request exception for '{url}' with - {exception}"
                ) from exception

            except asyncio.TimeoutError:
                raise UptimeRobotConnectionException(f"Request timeout for '{url}'")

            except UptimeRobotConnectionException as exception:
                raise UptimeRobotConnectionException(exception) from exception

            except UptimeRobotException as exception:
                raise UptimeRobotException(exception) from exception

            except (Exception, BaseException) as exception:
                raise UptimeRobotException(
                    f"Unexpected exception for '{url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", url, result)

            return UptimeRobotApiResponse.from_dict(
                {**result, "_api_path": api_path, "_method": method}
            )

        return wrapper

    return decorator
