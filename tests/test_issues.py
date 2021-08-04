"""Tests for Container."""

import asyncio
from pyuptimerobot.exceptions import UptimeRobotException
from unittest.mock import patch
from pyuptimerobot.models import APIStatus
import pytest
import aiohttp

from tests.common import fixture, TEST_API_TOKEN, TEST_RESPONSE_HEADERS
from pyuptimerobot import UptimeRobot, UptimeRobotConnectionException


@pytest.mark.asyncio
async def test_api_key_error(aresponses):
    """test_api_key_error."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/getMonitors",
        "post",
        aresponses.Response(
            text=fixture("bad_api_key", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_get_monitors()
        assert result.status == APIStatus.FAIL
        assert result.error.message == "api_key not found."


@pytest.mark.asyncio
async def test_bad_status_code(aresponses):
    """test_bad_status_code."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/getMonitors",
        "post",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=500,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        with pytest.raises(
            UptimeRobotConnectionException,
            match="Request for 'https://api.uptimerobot.com/v2/getMonitors' failed with status code '500'",
        ):
            result = await client.async_get_monitors()
            assert result is None


@pytest.mark.asyncio
async def test_client_error():
    """test_bad_status_code."""
    with patch("aiohttp.ClientSession._request", side_effect=aiohttp.ClientError):

        async with aiohttp.ClientSession() as session:
            client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
            with pytest.raises(UptimeRobotConnectionException):
                result = await client.async_get_monitors()
                assert result is None


@pytest.mark.asyncio
async def test_timeout_error():
    """test_timeout_error."""
    with patch("aiohttp.ClientSession._request", side_effect=asyncio.TimeoutError):

        async with aiohttp.ClientSession() as session:
            client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
            with pytest.raises(UptimeRobotConnectionException):
                result = await client.async_get_monitors()
                assert result is None


@pytest.mark.asyncio
async def test_uptime_robot_connection_exception():
    """test_uptime_robot_connection_exception."""
    with patch(
        "aiohttp.ClientSession._request", side_effect=UptimeRobotConnectionException
    ):

        async with aiohttp.ClientSession() as session:
            client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
            with pytest.raises(UptimeRobotConnectionException):
                result = await client.async_get_monitors()
                assert result is None


@pytest.mark.asyncio
async def test_uptime_robot_exception():
    """test_uptime_robot_exception."""
    with patch("aiohttp.ClientSession._request", side_effect=UptimeRobotException):

        async with aiohttp.ClientSession() as session:
            client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
            with pytest.raises(UptimeRobotException):
                result = await client.async_get_monitors()
                assert result is None


@pytest.mark.asyncio
async def test_exception():
    """test_uptime_robot_exception."""
    with patch("aiohttp.ClientSession._request", side_effect=Exception):

        async with aiohttp.ClientSession() as session:
            client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
            with pytest.raises(UptimeRobotException):
                result = await client.async_get_monitors()
                assert result is None
