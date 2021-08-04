"""Tests for Container."""

from pyuptimerobot.models import APIStatus
import pytest
import aiohttp

from tests.common import fixture, TEST_API_TOKEN, TEST_RESPONSE_HEADERS
from pyuptimerobot import UptimeRobot


@pytest.mark.asyncio
async def test_async_get_monitors(aresponses):
    """test_async_get_monitors."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/getMonitors",
        "post",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_get_monitors(**{"monitors": "123"})
        assert result.status == APIStatus.OK

        monitor = result.data[0]
        assert monitor.id == 777749809
