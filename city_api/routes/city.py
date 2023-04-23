

from fastapi import APIRouter, Query
from fastapi_sqlalchemy import db
from pydantic import parse_obj_as

from city_api.exceptions import ObjectNotFound, OSMCityNotFound
from city_api.models.db import City
from city_api.schemas.city import CityGet, CityPost
from city_api.utils.city import get_lat_lon, get_two_nearest


city = APIRouter(prefix="/city", tags=["City"])


@city.post("", response_model=CityGet)
async def add_city(city_inp: CityPost) -> CityGet:
    """
    Добавить город по имени, координаты добавляются автоматически
    :param city_inp: Модель города
    :return: CityGet - созданный город
    """
    lon, lat = await get_lat_lon(city_inp.name)
    if not lat or not lon:
        raise OSMCityNotFound(city_inp.name)
    db.session.add(_city := City(**city_inp.dict(), lat=lat, lon=lon))
    db.session.commit()
    return CityGet.from_orm(_city)


@city.get("/{id}", response_model=CityGet)
async def get_city(id: int) -> CityGet:
    """
    Получить город по айди
    :param id: Айди города
    :return: CityGet - полученный город
    """
    city = db.session.query(City).get(id)
    if not city:
        raise ObjectNotFound(City, id)
    return city


@city.get("", response_model=list[CityGet])
async def get_cities(lat: float = Query(default=None), lon: float = Query(default=None)) -> list[CityGet]:
    """
    Если переданы lat/lon, то вернет два ближайших города, в ином случае весь список
    :param lat: Широта
    :param lon: Долготвв
    :return: list[CityGet]
    """
    if lat is not None and lon is not None:
        return parse_obj_as(list[CityGet], await get_two_nearest(lat, lon))
    return parse_obj_as(list[CityGet], db.session.query(City).all())


@city.delete("/{id}", response_model=None)
async def delete_city(id: int) -> None:
    """
    Удалить город по айди
    :param id: айли удаляемого города
    :return: None
    """
    db.session.query(City).filter(City.id == id).delete()
    return None
