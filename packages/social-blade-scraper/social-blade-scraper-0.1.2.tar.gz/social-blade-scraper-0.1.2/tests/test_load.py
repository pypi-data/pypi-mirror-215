import asyncio

from src.social_blade_scraper.stats.youtube import youtube

from asyncio import sleep
from random import randint


async def test():
    time = randint(1, 3)
    await sleep(time / 10.0)

    for e in range(10):
        print(e)
        channel = await youtube(channel_name='mrfeast')
        await sleep(randint(1, 3))
        if channel:
            print(channel.profile)
        else:
            print('ERROR')


async def simulate_view():
    lists = []
    for e in range(60):
        lists.append(test())

    await asyncio.gather(*lists)


async def simulate_view_call():
    await simulate_view()


asyncio.run(simulate_view_call())
