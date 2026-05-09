"""Tests for Container."""

import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from pyuptimerobot import (
    UptimeRobot,
    UptimeRobotAuthenticationException,
    UptimeRobotConnectionException,
    UptimeRobotRateLimitException,
)
from pyuptimerobot.exceptions import UptimeRobotException
from tests.common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_api_key_error(aresponses):
    """test_api_key_error."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=401,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key="")
        with pytest.raises(UptimeRobotAuthenticationException):
            result = await client.async_get_monitors()
            assert result is None


@pytest.mark.asyncio
async def test_bad_status_code(aresponses):
    """test_bad_status_code."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
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
            match=(
                "Request for 'https://api.uptimerobot.com/v3/monitors'"
                " failed with status code '500'"
            ),
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
    with patch("aiohttp.ClientSession._request", side_effect=UptimeRobotConnectionException):
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


@pytest.mark.asyncio
async def test_rate_limit_with_headers(aresponses):
    """test_rate_limit_with_headers."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=429,
            headers={
                **TEST_RESPONSE_HEADERS,
                "X-RateLimit-Limit": "100",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "4",
                "Retry-After": "60",
            },
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        with pytest.raises(UptimeRobotRateLimitException) as exc_info:
            await client.async_get_monitors()

        exc = exc_info.value
        assert exc.limit == 100
        assert exc.remaining == 0
        assert exc.reset == 4
        assert exc.retry_after == 60
        assert exc.updated_at is not None
        assert client.ratelimit is not None
        assert client.ratelimit["limit"] == 100


@pytest.mark.asyncio
async def test_rate_limit_without_headers(aresponses):
    """test_rate_limit_without_headers."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=429,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        with pytest.raises(UptimeRobotRateLimitException) as exc_info:
            await client.async_get_monitors()

        exc = exc_info.value
        assert exc.limit is None
        assert exc.remaining is None
        assert exc.reset is None
        assert exc.retry_after is None
        assert exc.updated_at is not None


@pytest.mark.asyncio
async def test_ratelimit_on_success(aresponses):
    """test_ratelimit_on_success."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=200,
            headers={
                **TEST_RESPONSE_HEADERS,
                "X-RateLimit-Limit": "100",
                "X-RateLimit-Remaining": "99",
                "X-RateLimit-Reset": "4",
                "Retry-After": "0",
            },
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_get_monitors()

        assert client.ratelimit is not None
        assert client.ratelimit["limit"] == 100
        assert client.ratelimit["remaining"] == 99
        assert client.ratelimit["updated_at"] is not None

        assert result.ratelimit is not None
        assert result.ratelimit["limit"] == 100
        assert result.ratelimit["remaining"] == 99


@pytest.mark.asyncio
async def test_rate_limit_with_invalid_headers(aresponses):
    """test_rate_limit_with_invalid_headers."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v3/monitors",
        "get",
        aresponses.Response(
            text=fixture("getMonitors", False),
            status=429,
            headers={
                **TEST_RESPONSE_HEADERS,
                "X-RateLimit-Limit": "invalid",
                "X-RateLimit-Remaining": "abc",
                "X-RateLimit-Reset": "",
                "Retry-After": "not_a_number",
            },
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        with pytest.raises(UptimeRobotRateLimitException) as exc_info:
            await client.async_get_monitors()

        exc = exc_info.value
        assert exc.limit is None
        assert exc.remaining is None
        assert exc.reset is None
        assert exc.retry_after is None
