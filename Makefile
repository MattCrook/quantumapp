SHELL:=/bin/bash
REPO := quantumapp


venv_prep:
	source venv/bin/active

prep:
	pipenv sync --dev

prep_migrate:
	pipenv run python3 manage.py makemigrations

migrate: prep_migrate
	pipenv run python3 manage.py migrate

lock:
	pipenv lock

start_dev:
	pipenv run python3 manage.py runserver
