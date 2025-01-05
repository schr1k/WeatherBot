import aiohttp
from config import config


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
