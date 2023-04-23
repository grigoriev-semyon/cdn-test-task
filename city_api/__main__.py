import uvicorn

from city_api.routes.base import app


if __name__ == '__main__':
    uvicorn.run(app)
