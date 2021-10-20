SHELL:=/bin/bash
REPO := quantumapp


init_environment:
	@chmod +x ./scripts/init_environment.sh && ./scripts/init_environment.sh

venv_create:
	virtualenv venv

venv_init:
	source venv/bin/active

prep_sync:
	pipenv sync --dev

prep:
	pipenv install

prep_static:
	python3 manage.py collectstaic

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
	# pipenv run export DJANGO_ENV=local
	pipenv run python3 manage.py runserver --settings=quantumapp.dev_settings

docker_build_local:
	docker build -t quantumapp:latest .

docker_build_deploy:
	docker build \
		--build-arg DEPLOYED_FRONTEND_URI=https://quantum-coasters.uc.r.appspot.com/ \
		--build-arg DEPLOYED_BACKEND_URL=http://35.239.130.209 \
		-t quantumapp:latest .

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

run_local:
	# export DJANGO_ENV=local
	python3 manage.py runserver --settings=quantumapp.dev_settings
