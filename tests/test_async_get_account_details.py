"""Tests for Container."""

import aiohttp
import pytest

from pyuptimerobot import UptimeRobot
from pyuptimerobot.models import APIStatus
from tests.common import TEST_API_TOKEN, TEST_RESPONSE_HEADERS, fixture


@pytest.mark.asyncio
async def test_async_get_account_details(aresponses):
    """test_async_get_account_details."""
    aresponses.add(
        "api.uptimerobot.com",
        "/v2/getAccountDetails",
        "post",
        aresponses.Response(
            text=fixture("getAccountDetails", False),
            status=200,
            headers=TEST_RESPONSE_HEADERS,
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = UptimeRobot(session=session, api_key=TEST_API_TOKEN)
        result = await client.async_get_account_details()
        assert result.status == APIStatus.OK
        assert result.data.email == "test@domain.com"
