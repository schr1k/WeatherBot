import asyncio
import json
from datetime import datetime

import aiohttp
import config


async def get_weather_by_city(city) -> dict:
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'units': 'metric',
        'lang': 'ru',
        'appid': config.APP_ID
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def get_forecast_by_city(city) -> dict:
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'units': 'metric',
        'lang': 'ru',
        'appid': config.APP_ID
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def main():
    data = await get_forecast_by_city('Москва')
    print(json.dumps(await get_forecast_by_city('Москва'), indent=4, ensure_ascii=False))
    print(datetime.fromtimestamp(data['list'][-1]['dt']).strftime('%d.%m.%Y %H:%M'))

asyncio.run(main())
