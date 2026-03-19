"""Example usage of pyuptimerobot."""

import asyncio

import aiohttp

from pyuptimerobot import UptimeRobot

API_KEY = "u279802-9c317034ab9d67ffdc49ca2f"

TEST_ID = 801568845
TEST_STATUS = "pause"

async def example():
    """Example usage of pyuptimerobot."""
    async with aiohttp.ClientSession() as session:
        api = UptimeRobot(API_KEY, session)
        account = await api.async_get_account_details()
        monitors = await api.async_get_monitors()
        print("Account:", account)
        print("Monitors:", monitors)
        await api.async_edit_monitor(monitor_id=TEST_ID, status=TEST_STATUS)

asyncio.run(example())
