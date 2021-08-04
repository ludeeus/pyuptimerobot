"""Example usage of pyuptimerobot."""
import asyncio

import aiohttp

from pyuptimerobot import UptimeRobot

API_KEY = "ur432898-0acf29ba7b208ac5fa49e303"


async def example():
    """Example usage of pyhaversion."""
    async with aiohttp.ClientSession() as session:
        api = UptimeRobot(API_KEY, session)
        print((await api.async_get_monitors()))


loop = asyncio.get_event_loop()
loop.run_until_complete(example())
