"""Tests for edit monitor."""

import json

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotApiResponse, UptimeRobotMonitor

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.parametrize(
    "status",
    [
        "paused",
        "started",
        "up",
        "down",
    ],
)
@pytest.mark.asyncio
async def test_async_edit_monitor(aresponses, status):
    """test_async_edit_monitor."""

    fixture_data = fixture("editMonitor")
    fixture_data["status"] = status

    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors/1234",
        "patch",
        aresponses.Response(
            text=json.dumps(fixture_data),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_edit_monitor(monitor_id=1234, **{"status": status})
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)
        assert result.data.status == status
