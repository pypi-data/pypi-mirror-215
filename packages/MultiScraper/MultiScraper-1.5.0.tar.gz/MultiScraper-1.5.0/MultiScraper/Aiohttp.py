import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'lxml')
    return soup


async def get_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, cookies=cookies, json=json, data=data, params=params) as response:
            html = await response.text()

    return html


async def post_soup(url, headers={}, cookies={}, json={}, data={}, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'lxml')
    return soup


async def post_html(url, headers={}, cookies={}, json={}, data={}, params={}):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, cookies=cookies, json=json, data=data, params=params) as response:
            html = await response.text()

    return html