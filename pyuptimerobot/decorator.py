"""Decorator for Uptime Robot"""
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiohttp

from pyuptimerobot import exceptions

from .const import API_BASE_URL, API_HEADERS, LOGGER
from .models import APIStatus, UptimeRobotApiResponse

if TYPE_CHECKING:
    from .uptimerobot import UptimeRobot


def api_request(api_path: str, method: str = "POST"):
    """Decorator for Uptime Robot API request"""

    def decorator(func):
        """Decorator"""

        async def wrapper(*args, **kwargs):
            """Wrapper"""
            client: UptimeRobot = args[0]
            request_data = f"api_key={client._api_key}&format=json"
            url = f"{API_BASE_URL}{api_path}"
            if kwargs:
                for key, value in kwargs.items():
                    request_data += f"&{key}={value}"
            LOGGER.debug("Requesting %s", url)
            try:
                request = await client._session.request(
                    method=method,
                    url=url,
                    headers=API_HEADERS,
                    data=request_data,
                    timeout=aiohttp.ClientTimeout(total=10),
                )

                if request.status != 200:
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

            except exceptions.UptimeRobotException as exception:
                raise exceptions.UptimeRobotException(exception) from exception

            except (Exception, BaseException) as exception:
                raise exceptions.UptimeRobotException(
                    f"Unexpected exception for '{url}' with - {exception}"
                ) from exception

            LOGGER.debug("Requesting %s returned %s", url, result)

            response = UptimeRobotApiResponse.from_dict(
                {**result, "_api_path": api_path, "_method": method}
            )

            if response.status == APIStatus.FAIL:
                if response.error.message == "api_key parameter is missing.":
                    raise exceptions.UptimeRobotAuthenticationException(
                        "No API key was provided"
                    )
                elif response.error.message in (
                    "api_key not found.",
                    "api_key is invalid.",
                ):
                    raise exceptions.UptimeRobotAuthenticationException(
                        "The provided API key is not valid"
                    )

            return response

        return wrapper

    return decorator
