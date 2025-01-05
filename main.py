import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from config import config
from api import get_weather_by_city

bot = Bot(token=config.TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


@dp.message(Command('start'))
async def start(message: Message):
    await message.answer('Привет, я могу рассказать тебе о погоде.\n'
                         'Просто отправь название своего города.')


@dp.message()
async def get_weather(message: Message):
    weather = await get_weather_by_city(message.text)
    if weather['cod'] == '404' and weather['message'] == 'city not found':
        await message.answer('Город не найден.\n'
                             'Проверьте правильность написания.')
    else:
        city = message.text
        await message.answer(f'🌇 Сейчас в городе {city} {weather["weather"][0]["description"]}.\n'
                             f'🌡 Температура: {round(weather["main"]["temp"])} °C.\n'
                             f'💨 Ветер: {round(weather["wind"]["speed"], 1)} м/c.\n'
                             f'💦 Влажность: {weather["main"]["humidity"]} %.\n'
                             f'🧭 Давление: {round(weather["main"]["pressure"] * 0.750062)} мм рт. ст.')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
