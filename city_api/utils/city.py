import math

import aiohttp
from fastapi_sqlalchemy import db

from city_api.models.db import City
from city_api.settings import get_settings


settings = get_settings()


async def get_lat_lon(city_name: str) -> tuple[None, None] | tuple[float, float]:
    """
    Возвращает долготу и широту переданного города

    :param city_name: Название города

    :return: `tuple(долгота, широта)`
    """
    url = f"https://nominatim.openstreetmap.org"
    async with aiohttp.request("GET", url, params={"format": "json", "city": city_name, "limit": 1}) as r:
        status_code = r.status
        result = await r.json()
    if status_code != 200 or len(result) == 0:
        return None, None
    city = result[0]
    return float(city["lon"]), float(city["lat"])


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние на сфере между двумя точками

    :param lat1: Широта первой точки

    :param lon1: Долгота первой точки

    :param lat2: Широта второй точки

    :param lon2: Долгота второй точки

    :return: float - расстояние на сфере
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = 6371 * c

    return distance


async def get_two_nearest(lat: float, lon: float) -> list[City]:
    """
    Возвращает два ближайших города к заданной точке

    :param lat: Широта заданной точки

    :param lon: Долгота заданной точки

    :return: list[City] - список из двух ближайших городов
    """
    cities: list[City] = db.session.query(City).all()
    min_city1: City = cities[0] if len(cities) else None
    min_city2: City = cities[1] if len(cities) > 1 else None
    for city in cities:
        if (cur_dist := haversine_distance(lat, lon, city.lat, city.lon)) < haversine_distance(
            lat, lon, min_city1.lat, min_city1.lon
        ):
            min_city2 = min_city1
            min_city1 = city
        elif cur_dist < haversine_distance(lat, lon, min_city2.lat, min_city2.lon) and min_city1 != city:
            min_city2 = city
    return [min_city1, min_city2]
