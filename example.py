"""Example usage of pyuptimerobot."""
import asyncio

import aiohttp

from pyuptimerobot import UptimeRobot

API_KEY = ""


async def example():
    """Example usage of pyuptimerobot."""
    async with aiohttp.ClientSession() as session:
        api = UptimeRobot(API_KEY, session)
        account = await api.async_get_account_details()
        monitors = await api.async_get_monitors()
        print("Account:", account)
        print("Monitors:", monitors)


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
