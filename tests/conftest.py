import random

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from city_api.models.db import City
from city_api.routes.base import app
from city_api.settings import get_settings
from city_api.utils.utils import random_string


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture(scope='session')
def dbsession():
    settings = get_settings()
    engine = create_engine(settings.DB_DSN)
    TestingSessionLocal = sessionmaker(bind=engine)
    yield TestingSessionLocal()


@pytest.fixture
def city(dbsession):
    cities = []

    def _city():
        nonlocal cities
        dbsession.add(__city := City(name=random_string(), lon=random.random(), lat=random.random()))
        dbsession.commit()
        cities.append(__city)
        return __city
    yield _city
    for __city in cities:
        dbsession.delete(__city)
    dbsession.commit()

