from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from city_api import __version__
from city_api.settings import get_settings

from .city import city


settings = get_settings()
app = FastAPI(
    title='Сервис горододв',
    description='Сервис для хранения информации о городах и работы с ней',
    version=__version__,
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url=None if __version__ != 'dev' else '/docs',
    redoc_url=None,
)


app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.DB_DSN,
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.include_router(city)
