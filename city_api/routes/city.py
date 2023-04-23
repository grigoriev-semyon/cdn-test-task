from fastapi import APIRouter
from fastapi_sqlalchemy import db
from pydantic import parse_obj_as

from city_api.exceptions import ObjectNotFound, OSMCityNotFound
from city_api.models.db import City
from city_api.schemas.city import CityGet, CityPost, LatLon
from city_api.utils.city import get_lat_lon, get_two_nearest


city = APIRouter(prefix="/city", tags=["City"])


@city.post("", response_model=CityGet)
async def add_city(city_inp: CityPost) -> CityGet:
    lat, lon = await get_lat_lon(city_inp.name)
    if not lat or not lon:
        raise OSMCityNotFound(city_inp.name)
    db.session.add(_city := City(**city_inp.dict(), lat=lat, lon=lon))
    db.session.commit()
    return CityGet.from_orm(_city)


@city.get("/{id}", response_model=CityGet)
async def get_city(id: int) -> CityGet:
    city = db.session.query(City).get(id)
    if not city:
        raise ObjectNotFound(City, id)
    return city


@city.get("", response_model=list[CityGet])
async def get_cities() -> list[CityGet]:
    return parse_obj_as(list[CityGet], db.session.query(City).all())


@city.delete("/{id}", response_model=None)
async def delete_city(id: int) -> None:
    db.session.query(City).filter(City.id == id).delete()
    return None


@city.post("/nearest", response_model=list[CityGet])
async def get_two_nearest_cities(lat_lon_inp: LatLon) -> list[CityGet]:
    return parse_obj_as(list[CityGet], await get_two_nearest(lat_lon_inp.lat, lat_lon_inp.lon))
