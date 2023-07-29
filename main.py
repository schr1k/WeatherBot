import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config
from support import get_weather_by_city

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(filename="all_log.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warning_log = logging.getLogger("warning_log")
warning_log.setLevel(logging.WARNING)
fh = logging.FileHandler("warning_log.log")
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(funcName)s: %(message)s (%(lineno)d)')
fh.setFormatter(formatter)
warning_log.addHandler(fh)


# Главная ==============================================================================================================
@dp.message_handler(commands=['start'])
async def start(message):
    try:
        await message.answer('Привет, я могу рассказать тебе о погоде.\n'
                             'Просто отправь название своего города.')
    except Exception as e:
        warning_log.warning(e)


@dp.message_handler(content_types=['text'])
async def get_weather(message):
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
        warning_log.warning(e)


if __name__ == '__main__':
    print('Работаем👌')
    executor.start_polling(dp, skip_updates=False)
