from typing import Type


class OSMCityNotFound(Exception):
    def __init__(self, name: str):
        super().__init__(f"City {name=} not found")


class ObjectNotFound(Exception):
    def __init__(self, type: Type, id: int):
        super().__init__(f"Object {type.__name__} {id=} not found")
