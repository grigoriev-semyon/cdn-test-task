run:
	source ./venv/bin/activate && uvicorn --reload --log-config logging_dev.conf city_api.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./city_api
	isort ./city_api
	black ./city_api

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-city_api postgres:latest

env:
	touch .env && echo "DB_DSN=postgresql://postgres@localhost:5432/postgres" >> .env

migrate:
	alembic upgrade head
