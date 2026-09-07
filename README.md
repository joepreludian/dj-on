# 🚀 DJ-ON
An opinionated cookiecutter project template for Django quickstart. It's using some common technologies that helps to bootstrap a production ready django application.

## 🔩 Features

- **PostgreSQL** via `psycopg2-binary`
- **Daphne** ASGI server (also powers `manage.py runserver`)
- **django-environ** for 12-factor config
- **WhiteNoise** for static files
- **django-ninja** with a `/api/healthcheck/` endpoint pre-wired
- **Docker Compose** + multi-stage `Dockerfile`
- **Makefile** with common development targets
- **Dramatiq + Valkey** — task queue and worker service
- **APScheduler** via `django-apscheduler` — scheduled jobs in a dedicated `scheduler` service, with job and execution history in the Django admin
- **pre-commit** with Ruff (linting + formatting) and common hooks
- **Jazzmin** for a modern Django Admin interface
- **django-cors-headers** pre-configured for development
- **`base` app** pre-scaffolded to work as a support app for your apps.
  - Contains a healthcheck API route and a common Abstract model with `created_at` and `updated_at` fields. 
- **tests** folder with functional and unit tests using `pytest`


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
3. Initialises a git repository and creates an initial commit
4. Builds Docker images (`docker compose build --no-cache`)
5. Starts Docker Compose services (`docker compose up --wait`)
6. Applies database migrations (`make migrate`)
7. Prepares translations (`make messages` and `make compilemessages`)
8. Creates a superuser (`make createsuperuser`)
9. Installs and runs `pre-commit` hooks

Once complete, your project is ready:

```bash
cd <project_slug>
```
And start doing your great new application!

# Check the API documentation
http://localhost:<app_container_port>/api/docs

# Check the health endpoint
http://localhost:<app_container_port>/api/healthcheck/

Healthcheck API endpoint generates a simple output:
```json
{
    "status": "ok",
    "api_version": "<project_version>",
    "commit": "<commit_sha>"
}
```
It doesn't test for database connectivity or other health checks. You should implement your own check service.

### Common Makefile targets

```bash
make runserver       # Start the dev server via Daphne
make migrate         # Apply database migrations
make migrations      # Create new migrations
make createsuperuser # Create a Django superuser
make scheduler       # Run the APScheduler process in the foreground
make test            # Run tests with pytest
make shell           # Open the Django interactive shell
make dbshell         # Open the database shell
make check           # Run Django system checks
make messages        # Generate translation files
make compilemessages # Compile translation files
make build           # Build Docker images
make up              # Start all services (detached)
make down            # Stop all services
make logs            # Follow Docker Compose logs
make clean           # Stop containers, remove volumes, clean pycache
make destroy_and_recreate_all_migrations # DESTROY EVERYTHING, RECREATE ALL MIGRATIONS AND DB (DEV ONLY)
```

### ⏰ Scheduled jobs

Scheduled work runs in its own `scheduler` container (`python manage.py run_apscheduler`),
separate from the Dramatiq `worker`.

Any app can schedule jobs by adding a `jobs.py` that exposes `register(scheduler)` —
the same convention django-dramatiq uses for `tasks.py`. The command discovers it
automatically, so it never needs editing:

```python
# src/orders/jobs.py
from apscheduler.triggers.cron import CronTrigger

from orders.tasks import sync_orders


def register(scheduler):
    scheduler.add_job(
        sync_orders.send,
        trigger=CronTrigger(minute="*/15"),
        id="orders.sync_orders",
        max_instances=1,
        replace_existing=True,
    )
```

`src/base/jobs.py` ships a working example that prunes old execution history.

**Two constraints worth knowing:**

1. The scheduler must run as **exactly one process**. Scaling it fires every job
   once per replica. That is why it is its own service rather than part of `worker`.
2. Schedule the *enqueue*, not the work. A slow job blocks every other job in that
   single process, so jobs should call a Dramatiq actor's `.send()` and let the
   scalable worker do the actual work.

Jobs and their run history are visible in the Django admin under **Django APScheduler**.

### 💣 Destroy and Recreate All Migrations

This project includes a special Makefile target to help you during the initial development phase when you are still iterating on your models and don't want to keep a long history of migrations.

```bash
make destroy_and_recreate_all_migrations
```

**What it does:**
1. Prompts for confirmation (it's a destructive action!).
2. Deletes all migration files (`0*.py`) in your project.
3. Cleans up the Docker Compose environment (removes volumes, including the database).
4. Re-runs `makemigrations` to create a fresh initial migration.
5. Applies the new migration.
6. Prompts to create a new superuser.

**⚠️ Warning:** This command is intended for **development only**. It will delete all data in your local database. Never use this in production or on a shared database.