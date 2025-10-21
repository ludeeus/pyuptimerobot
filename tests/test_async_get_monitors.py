"""Tests for Container."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot
from pyuptimerobot.models import APIStatus, UptimeRobotMonitor
from tests.common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_get_monitors(aresponses):
    """test_async_get_monitors."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_get_monitors(**{"monitors": "123"})
        assert isinstance(result.data, list) and all(
            isinstance(m, UptimeRobotMonitor) for m in result.data
        )
        monitor = result.data[0]
        assert monitor.id == 0
