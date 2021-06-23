prep:
	source venv/bin/active

prep_migrate:
	python manage.py makemigrations

migrate: prep_migrate
	python manage.py migrate
