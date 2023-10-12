import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters.command import Command

import config
from api import get_weather_by_city

bot = Bot(token=config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(filename="all.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
errors = logging.getLogger("errors")
errors.setLevel(logging.ERROR)
fh = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s function: %(funcName)s line: %(lineno)d - %(message)s')
fh.setFormatter(formatter)
errors.addHandler(fh)


# Главная ==============================================================================================================
@dp.message(Command('start'))
async def start(message: Message):
    try:
        await message.answer('Привет, я могу рассказать тебе о погоде.\n'
                             'Просто отправь название своего города.')
    except Exception as e:
        errors.warning(e)


# Погода ===============================================================================================================
@dp.message()
async def get_weather(message: Message):
    try:
        weather = get_weather_by_city(message.text)
        if weather['cod'] == '404' and weather['message'] == 'city not found':
            await message.answer('Город не найден.\n'
                                 'Проверьте правильность написания.')
        else:
            city = message.text
            if city[-1] == 'й':
                city = city[:-2] + 'ом'
            elif city[-1] == 'ы':
                city = city[:-2] + 'ах'
            elif city[-1] == 'у':
                pass
            elif city[-1] in ['а', 'о', 'е', 'э', 'я', 'и', 'ю']:
                city = city[:-1] + 'е'
            else:
                city = city + 'е'
            await message.answer(f'🌇 Сейчас в {city} {weather["weather"][0]["description"]}.\n'
                                 f'🌡 Температура: {round(weather["main"]["temp"])} °C.\n'
                                 f'💨 Ветер: {round(weather["wind"]["speed"], 1)} м/c.\n'
                                 f'💦 Влажность: {weather["main"]["humidity"]} %.\n'
                                 f'🧭 Давление: {round(weather["main"]["pressure"] * 0.750062)} мм рт. ст.')
    except Exception as e:
        errors.warning(e)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print(f'Бот запущен ({datetime.now().strftime("%H:%M:%S %d.%m.%Y")}).')
    asyncio.run(main())
