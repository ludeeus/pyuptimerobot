"""Tests for Container."""

import json

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotApiResponse, UptimeRobotMonitor
from pyuptimerobot.const import (
    API_MONITOR_ACTION_PAUSE,
    API_MONITOR_ACTION_START,
    API_STATUS_DOWN,
    API_STATUS_PAUSED,
    API_STATUS_STARTED,
    API_STATUS_UP,
)

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.parametrize(
    ("api_status", "action", "status"),
    [
        (API_STATUS_PAUSED, API_MONITOR_ACTION_START, API_STATUS_STARTED),
        (API_STATUS_STARTED, API_MONITOR_ACTION_PAUSE, API_STATUS_PAUSED),
        (API_STATUS_UP, API_MONITOR_ACTION_PAUSE, API_STATUS_PAUSED),
        (API_STATUS_DOWN, API_MONITOR_ACTION_PAUSE, API_STATUS_PAUSED),
    ],
)
@pytest.mark.asyncio
async def test_async_edit_monitor(aresponses, api_status, action, status):
    """test_async_edit_monitor."""

    fixture_data = fixture("editMonitor")
    fixture_data["status"] = status

    aresponses.add(
        "api.uptimerobot.com",
        f"/v3/monitors/1234/{action}",
        "post",
        aresponses.Response(
            text=json.dumps(fixture_data),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_edit_monitor(monitor_id=1234, **{"status": api_status})
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)
        assert result.data.status == status
