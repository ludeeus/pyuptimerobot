"""Example usage of pyuptimerobot."""

import asyncio
import os

import aiohttp

from pyuptimerobot import UptimeRobot


async def example():
    """Example usage of pyuptimerobot."""
    if (api_key := os.getenv("UPTIMEROBOT_API_KEY")) is None:
        print("Please set the UPTIMEROBOT_API_KEY environment variable.")
        return
    async with aiohttp.ClientSession() as session:
        api = UptimeRobot(api_key, session)
        account = await api.async_get_account_details()
        monitors = await api.async_get_monitors()
        print("Account:", account)
        print("Monitors:", monitors)


asyncio.run(example())
