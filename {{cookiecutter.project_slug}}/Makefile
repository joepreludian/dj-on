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

test:
	$(RUN_APP) pytest

destroy_and_recreate_all_migrations:
	@read -p "THIS WILL REMOVE ALL MIGRATIONS AND RECREATE ALL THE DB STRUCTURE. MUST ONLY BE USED IN DEV. ARE YOU SURE? [y/n]: " ANSWER; \
	if [ "$$ANSWER" != "y" ]; then \
		echo "Operation cancelled."; \
		exit 1; \
	fi

	@echo "Removing old migrations..."
	find ./src -name "0*.py" | grep migrations | xargs rm -v

	$(MAKE) clean
	$(MAKE) migrations
	$(MAKE) migrate
	$(MAKE) createsuperuser

