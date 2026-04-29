"""Tests for monitor action methods (pause, start, reset)."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot, UptimeRobotApiResponse, UptimeRobotMonitor

from .common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_pause_monitor(aresponses):
    """test_async_pause_monitor."""

    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors/1234/pause",
        "post",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_pause_monitor(monitor_id=1234)
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)


@pytest.mark.asyncio
async def test_async_start_monitor(aresponses):
    """test_async_start_monitor."""

    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors/1234/start",
        "post",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_start_monitor(monitor_id=1234)
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)


@pytest.mark.asyncio
async def test_async_reset_monitor(aresponses):
    """test_async_reset_monitor."""

    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors/1234/reset",
        "post",
        aresponses.Response(
            text=fixture("editMonitor", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_reset_monitor(monitor_id=1234)
        assert isinstance(result, UptimeRobotApiResponse)
        assert isinstance(result.data, UptimeRobotMonitor)
