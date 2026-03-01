RUN_APP = docker compose run --rm app
DJANGO_CMD = $(RUN_APP) python manage.py

runserver:
	$(DJANGO_CMD) runserver

migrate:
	$(DJANGO_CMD) migrate

migrations:
	$(DJANGO_CMD) makemigrations

collectstatic:
	$(DJANGO_CMD) collectstatic --noinput

createsuperuser:
	$(DJANGO_CMD) createsuperuser

shell:
	$(DJANGO_CMD) shell

dbshell:
	$(DJANGO_CMD) dbshell

check:
	$(DJANGO_CMD) check

messages:
	$(DJANGO_CMD) makemessages -l {{ cookiecutter.i18n_language_code}}

compilemessages:
	$(DJANGO_CMD) compilemessages -l {{ cookiecutter.i18n_language_code}}

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v

tests:
	$(RUN_APP) cd .. && pytest

