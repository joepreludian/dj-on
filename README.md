# django-init

A [cookiecutter](https://github.com/cookiecutter/cookiecutter) template for production-ready Django projects.

## Features

- **PostgreSQL** via `psycopg2-binary`
- **Daphne** ASGI server (also powers `manage.py runserver`)
- **django-environ** for 12-factor config
- **WhiteNoise** for static files
- **django-ninja** with a `/api/health` endpoint pre-wired
- **uv** package manager with `src/` layout
- **Docker Compose** + multi-stage `Dockerfile`
- **Makefile** with common development targets
- **Dramatiq + Valkey** — task queue and worker service, always included
- **pre-commit** with Ruff (linting + formatting) and common hooks
- **`base` app** pre-scaffolded as a starter Django app

## Requirements

- [cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter` or `uv tool install cookiecutter`)
- [uv](https://docs.astral.sh/uv/) (installed on your machine)
- [Docker](https://docs.docker.com/get-docker/) (for the post-generation setup)

## Usage

```bash
cookiecutter gh:preludian/django-init
```

Or locally:

```bash
cookiecutter path/to/django-init
```

### Prompts

| Variable | Default | Description |
|---|---|---|
| `project_name` | My Django Project | Human-readable project name |
| `project_slug` | auto-derived | Python package name (underscored) |
| `description` | A Django project | Short description |
| `author_name` | Your Name | Author name |
| `author_email` | your@email.com | Author email |
| `python_version` | 3.13 | Python version |
| `language_code` | en-us | Django `LANGUAGE_CODE` setting |
| `timezone` | UTC | Django `TIME_ZONE` setting |
| `app_container_port` | 8001 | Host port mapped to the app container |

## After Generation

The post-generation hook runs automatically and:

1. Creates `.env` from `.env.example` with a generated `SECRET_KEY`
2. Runs `uv sync` to install dependencies
3. Initialises a git repository
4. Builds Docker images (`docker compose build --no-cache`)
5. Starts Docker Compose services (`docker compose up --wait`)
6. Applies database migrations (`make migrate`)

Once complete, your project is ready:

```bash
cd <project_slug>

# Check the health endpoint
curl http://localhost:<app_container_port>/api/health
# → {"status": "ok"}
```

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

## Generated Project Structure

```
<project_slug>/
├── .env.example
├── .env               ← created by hook with generated SECRET_KEY
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
├── uv.lock            ← created by hook after uv sync
├── Makefile
├── app.Dockerfile
├── docker-compose.yml
└── src/
    ├── manage.py
    ├── base/          ← starter app (models, views, admin, tests)
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── migrations/
    │   ├── models.py
    │   ├── tests.py
    │   └── views.py
    └── <project_slug>/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py
```
