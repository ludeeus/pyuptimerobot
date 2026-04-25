"""Tests for Container."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotApiResponse, UptimeRobotMonitor
from pyuptimerobot.const import API_MONITOR_ACTION_PAUSE, API_STATUS_PAUSED

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_edit_monitor(aresponses):
    """test_async_edit_monitor."""
    aresponses.add(
        "api.uptimerobot.com",
        f"/v3/monitors/1234/{API_MONITOR_ACTION_PAUSE}",
        "post",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_edit_monitor(monitor_id=1234, **{"status": API_STATUS_PAUSED})
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)
        assert result.data.status == API_STATUS_PAUSED
