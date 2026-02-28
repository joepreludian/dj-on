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
- **Dramatiq + Redis** — optional (prompted at generation time)

## Requirements

- [cookiecutter](https://cookiecutter.readthedocs.io/) (`pip install cookiecutter` or `uv tool install cookiecutter`)
- [uv](https://docs.astral.sh/uv/) (installed on your machine)

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
| `use_dramatiq` | n | Include Dramatiq + Redis task queue (`y`/`n`) |

## After Generation

```bash
cd <project_slug>

# .env was created by the post-gen hook; review and update DATABASE_URL
# then run:
make migrate
make runserver

# Check the health endpoint
curl http://localhost:8000/api/health
# → {"status": "ok"}
```

### Docker

```bash
make build
make up
make logs
```

## Generated Project Structure

```
<project_slug>/
├── .env.example
├── .env               ← created by hook with generated SECRET_KEY
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock            ← created by hook after uv sync
├── Makefile
├── Dockerfile
├── docker-compose.yml
└── src/
    ├── manage.py
    └── <project_slug>/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py
```
