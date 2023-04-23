import pytest
import sqlalchemy.exc

from city_api.models.db import City
from city_api.utils.utils import random_string


def test_create(client, dbsession):
    resp = client.post("/city", json={"name": "Moscow"})
    assert resp.status_code == 200
    assert resp.json()
    assert resp.json()["name"] == "Moscow"
    assert int(resp.json()["lat"]) == 55
    assert int(resp.json()["lon"]) == 37
    dbsession.query(City).filter(City.id == resp.json()["id"]).delete()


def test_get(client, dbsession, city):
    _city = city()
    resp = client.get(f"/city/{_city.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == _city.name
    assert resp.json()["id"] == _city.id
    assert resp.json()["lon"] == float(_city.lon)
    assert resp.json()["lat"] == float(_city.lat)


def test_get_all(client, dbsession, city):
    city1 = city()
    city2 = city()
    resp = client.get("/city")
    assert resp.status_code == 200
    assert {"id": city1.id, "name": city1.name, "lat": float(city1.lat), "lon":float(city1.lon)} in resp.json()
    assert {"id": city2.id, "name": city2.name, "lat": float(city2.lat), "lon": float(city2.lon)} in resp.json()


def test_delete(client, dbsession):
    resp = client.post("/city", json={"name": "Moscow"})
    id = resp.json()["id"]
    resp = client.delete(f"/city/{id}")
    assert resp.status_code == 200
    resp = client.get(f"/city/{id}")
    assert resp.status_code == 404
    with pytest.raises(sqlalchemy.exc.NoResultFound):
        dbsession.query(City).filter(City.id == id).one()



def test_get_nearest(client, dbsession):
    dbsession.add(city1 := City(name=random_string(), lat=0.1, lon=0.1))
    dbsession.add(city2 := City(name=random_string(), lat=0.5, lon=0.5))
    dbsession.add(city3 := City(name=random_string(), lat=2.1, lon=2.1))
    dbsession.commit()
    resp = client.get("/city", params={"lat": 0.3, "lon": 0.3})
    assert resp.status_code == 200
    assert {"id": city1.id, "name": city1.name, "lat": float(city1.lat), "lon":float(city1.lon)} in resp.json()
    assert {"id": city2.id, "name": city2.name, "lat": float(city2.lat), "lon":float(city2.lon)} in resp.json()
    assert {"id": city3.id, "name": city3.name, "lat": float(city3.lat), "lon":float(city3.lon)} not in resp.json()
    for city in (city1, city2, city3):
        dbsession.delete(city)
    dbsession.commit()


