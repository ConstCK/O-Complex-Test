import datetime
from typing import Any

import requests
from .models import ForecastOrder

CITY_COORDS_URL = 'https://geocoding-api.open-meteo.com/v1/search'
WEATHER_FORECAST_URL = 'https://api.open-meteo.com/v1/forecast'


def get_coords_from_db(city_name: str) -> dict[str, str] | None:
    result = ForecastOrder.objects.filter(city=city_name)
    if result:
        return {'latitude': result[0].city_lat, 'longitude': result[0].city_lon}


def get_coords_by_city(city_name: str) -> dict[str, str] | None:
    # Получение координат города по его названию с API
    params = {
        'name': city_name,
        'language': 'ru',
        'count': 1,
    }
    try:
        response = requests.get(
            CITY_COORDS_URL, params=params).json().get('results')[0]
        lat = response.get('latitude')
        lon = response.get('longitude')
        return {'latitude': lat, 'longitude': lon}
    except Exception:
        return None


def get_weather_forecast(lat: str, lon: str) -> dict[str, int] | None:
    # Получение температуры на ближайший час по координатам города с API
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }
    try:
        response = requests.get(WEATHER_FORECAST_URL,
                                params=params).json()
        current_time = datetime.datetime.now().hour
        # Список всех временных отрезков суток
        time_list = response.get('hourly').get('time')
        # Перевод в datetime формат
        time_obj_list = list(map(lambda x: datetime.datetime.strptime(
            x, '%Y-%m-%dT%H:%M'), time_list))
        # Выбор часа больше текущего
        forecast_time = [x for x in time_obj_list if x.hour > current_time][0]
        forecast_hour = forecast_time.hour
        # Выбор температуры на ближайший час
        forecast_temp = response.get('hourly').get(
            'temperature_2m')[forecast_hour]
        return {'hour': forecast_hour, 'temperature': forecast_temp}

    except Exception:
        return None


def add_data_to_db(user: str, city_name: str, lat: str, lon: str, ) -> None:
    # Добавление запроса погоды в БД
    ForecastOrder.objects.create(user=user, city=city_name, city_lat=lat, city_lon=lon)


def last_city_info(user: str) -> str | None:
    # Получение города из последнего запроса пользователя
    result = ForecastOrder.objects.filter(user=user)
    if result:
        return result[0].city


def get_statistic(user: str) -> list[dict[str, Any]] | None:
    # Получение статистики запросов пользователя

    query = ForecastOrder.objects.filter(user=user)
    if query:
        result = [x for x in query.values('city', 'created_at')]
        return result
