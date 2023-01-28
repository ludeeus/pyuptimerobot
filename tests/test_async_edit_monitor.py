"""Tests for Container."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot
from pyuptimerobot.models import APIStatus

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_edit_monitor(aresponses):
    """test_async_edit_monitor."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/editMonitor",
        "post",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_edit_monitor(monitor_id=777749809, **{"status": 0})
        assert result.status == APIStatus.OK
