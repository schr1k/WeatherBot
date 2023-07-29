import requests
import config


def get_weather_by_city(city):
    weather_json = requests.get('https://api.openweathermap.org/data/2.5/weather',
                                params={
                                    'q': city,
                                    'units': 'metric',
                                    'lang': 'ru',
                                    'appid': config.APP_ID}
                                ).json()
    return weather_json


def get_forecast_by_city(city):
    forecast_json = requests.get('https://api.openweathermap.org/data/2.5/forecast',
                                 params={'q': city,
                                         'units': 'metric',
                                         'lang': 'ru',
                                         'appid': config.APP_ID}
                                 ).json()
    return forecast_json
