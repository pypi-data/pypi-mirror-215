import asyncio

from fake_useragent import UserAgent
from httpx import AsyncClient, Response
import random

# from fp.fp import FreeProxy
#
#
# class ProxyManager:
#     PROXY_UPDATE_COUNT = 10
#
#     def __init__(self):
#         self._counter = 0
#         self._proxy = FreeProxy(https=True, timeout=0.1).get()
#
#     def get_proxy(self):
#         self._counter += 1
#
#         if self._counter >= self.PROXY_UPDATE_COUNT:
#             self.__init__()
#
#         return self._proxy[len('http://'):]
#
#
# proxy_manager = ProxyManager()
#
#
# def build_proxy_dict(proxy_address: str) -> dict:
#     return {
#         'http://': f'http://{proxy_address}',
#         'https://': f'https://{proxy_address}'
#     }
#
#
# proxy = proxy_manager.get_proxy()
# proxies = build_proxy_dict(proxy)
# print(proxies)
import httpx

# Use same client for fetching page faster for same host
limits = httpx.Limits(max_keepalive_connections=100, max_connections=100)
client = AsyncClient(timeout=30, limits=limits)


async def default_fetch(target_url: str, params: dict = None, extra_headers: dict = None) -> Response:
    # Create a UserAgent object
    user_agent = UserAgent()

    # Generate a random user agent string for Firefox
    firefox_user_agent = user_agent.firefox

    headers = {
        "User-Agent": firefox_user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    if extra_headers:
        headers = {**headers, **extra_headers}

    res = await client.get(target_url, params=params, headers=headers)
    return res


fetch = default_fetch
