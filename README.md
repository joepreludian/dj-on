# 🚀 DJ-ON
An opinionated cookiecutter project template for Django quickstart. It's using some common technologies that helps to bootstrap a production ready django application.

## 🔩 Features

- **PostgreSQL** via `psycopg2-binary`
- **Daphne** ASGI server (also powers `manage.py runserver`)
- **django-environ** for 12-factor config
- **WhiteNoise** for static files
- **django-ninja** with a `/api/health` endpoint pre-wired
- **Docker Compose** + multi-stage `Dockerfile`
- **Makefile** with common development targets
- **Dramatiq + Valkey** — task queue and worker service
- **pre-commit** with Ruff (linting + formatting) and common hooks
- **`base` app** pre-scaffolded to work as a support app for your apps.
  - Contains a healthcheck API route and a common Abstract model with created_at and updated_at fields. 
- **tests** folder


## 📝 Requirements

- [cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter` or `uv tool install cookiecutter`)
- [uv](https://docs.astral.sh/uv/) (installed on your machine)
- [Docker](https://docs.docker.com/get-docker/) (for the post-generation setup)

## ▶️ Start here

```bash
cookiecutter gh:preludian/django-init
```

Or locally:

```bash
cookiecutter path/to/django-init
```

## 🪖 After Generation

The post-generation hook runs automatically and:

1. Creates `.env` from `.env.example` with a generated `SECRET_KEY`
2. Runs `uv sync` to install dependencies
3. Initialises a git repository
4. Builds Docker images (`docker compose build --no-cache`)
5. Starts Docker Compose services (`docker compose up --wait`)
6. Applies database migrations (`make migrate`)
7. Creates a superuser (`make createsuperuser`)

Once complete, your project is ready:

```bash
cd <project_slug>
```
And start doing your great new application!

# Check the health endpoint
http://localhost:<app_container_port>/api/docs

### Common Makefile targets

```bash
make runserver       # Start the dev server via Daphne
make migrate         # Apply database migrations
make makemigrations  # Create new migrations
make createsuperuser # Create a Django superuser
make shell           # Open the Django interactive shell
make dbshell         # Open the database shell
make check           # Run Django system checks
make build           # Build Docker images
make up              # Start all services (detached)
make down            # Stop all services
make logs            # Follow Docker Compose logs
make clean           # Stop containers, remove volumes, clean pycache
```