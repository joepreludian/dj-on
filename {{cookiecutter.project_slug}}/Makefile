.DEFAULT_GOAL := help

.PHONY: help setup env runserver migrate makemigrations collectstatic createsuperuser shell dbshell check build up down logs ps clean clean-pyc worker

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

env: ## Copy .env.example to .env if .env does not exist
	@test -f .env || cp .env.example .env && echo ".env created from .env.example"

runserver: ## Start development server (via Daphne)
	docker compose run --rm app python manage.py runserver

migrate: ## Apply database migrations
	docker compose run --rm app python manage.py migrate

makemigrations: ## Create new migrations
	docker compose run --rm app python manage.py makemigrations

collectstatic: ## Collect static files
	docker compose run --rm app python manage.py collectstatic --noinput

createsuperuser: ## Create a Django superuser
	docker compose run --rm app python manage.py createsuperuser

shell: ## Open Django interactive shell
	docker compose run --rm app python manage.py shell

dbshell: ## Open database shell
	docker compose run --rm app python manage.py dbshell

check: ## Run Django system checks
	docker compose run --rm app python manage.py check

build: ## Build Docker images
	docker compose build

up: ## Start Docker Compose services (detached)
	docker compose up -d

down: ## Stop Docker Compose services
	docker compose down

logs: ## Follow Docker Compose logs
	docker compose logs -f

clean: ## Stop containers, remove volumes, and clean pycache
	docker compose down -v
	$(MAKE) clean-pyc

clean-pyc: ## Remove Python cache files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
