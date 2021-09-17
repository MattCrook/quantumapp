SHELL:=/bin/bash
REPO := quantumapp


venv_create:
	virtualenv venv

venv_init:
	source venv/bin/active

prep_sync:
	pipenv sync --dev

prep:
	pipenv install

prep_migrate:
	pipenv run python3 manage.py makemigrations

migrate: prep_migrate
	pipenv run python3 manage.py migrate

venv_migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

lock:
	pipenv lock

start_dev:
	pipenv run python3 manage.py runserver

docker_build:
	docker build -t quantumapp:latest .

docker_run:
	docker run -it -d --env-file .env -p 8000:8000 quantumapp

docker_compose:
	docker-compose up --build

dockerhub_tag:
	docker tag $(image):latest $(DOCKERHUB_REPO):$(tag)

dockerhub_push:
	docker push $(DOCKERHUB_REPO):$(tag)

venv_test:
	python3 manage.py test

test:
	pipenv run python3 manage.py test
