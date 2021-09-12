ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose build

rebuild-api:
	docker-compose up -d --no-deps --build api

up:
	docker-compose up --remove-orphans

down:
	docker-compose down

makemigrations:
	docker-compose run api sh -c "python manage.py makemigrations"

# migrate part of start up so only makemigrations needed
# superuser created on start up

# Remove all volumes
down-v:
	docker-compose down -v

volume:
	docker volume inspect iconnect-src_postgres_data