from pydantic import constr

from .base import Base


class CityPost(Base):
    name: constr(min_length=1)


class LatLon(Base):
    lon: float
    lat: float


class CityGet(CityPost, LatLon):
    id: int
