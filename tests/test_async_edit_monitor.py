"""Tests for Container."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotApiResponse, UptimeRobotMonitor
from pyuptimerobot.models import APIStatus

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_edit_monitor(aresponses):
    """test_async_edit_monitor."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors/1234",
        "patch",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    status = "paused"

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_edit_monitor(monitor_id=1234, **{"status": status})
        assert isinstance(result, UptimeRobotApiResponse)
        assert result.data[0].status == status
