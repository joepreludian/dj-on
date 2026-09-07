"""Scheduler construction and per-app job discovery.

Kept out of the management command so both halves can be exercised in tests
without starting a blocking process.
"""

import logging
from importlib import import_module

from apscheduler.schedulers.blocking import BlockingScheduler
from django.apps import apps
from django.conf import settings
from django.utils.module_loading import module_has_submodule
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger(__name__)

JOBS_MODULE_NAME = "jobs"


def create_scheduler() -> BlockingScheduler:
    """Build the scheduler used by the `run_apscheduler` command.

    Jobs are persisted through DjangoJobStore, so the schedule and its execution
    history are visible in the Django admin. The store only touches the database
    once the scheduler starts, not here.
    """
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    return scheduler


def register_jobs(scheduler) -> list[str]:
    """Import every installed app's `jobs` module and let it register its jobs.

    Each app that schedules work declares a `jobs.py` exposing
    `register(scheduler)`, mirroring how django-dramatiq picks up `tasks.py`.
    Returns the module paths that registered, for logging and tests.
    """
    registered = []

    for app_config in apps.get_app_configs():
        if not module_has_submodule(app_config.module, JOBS_MODULE_NAME):
            continue

        module_path = f"{app_config.name}.{JOBS_MODULE_NAME}"
        # Import errors raised from inside the module are deliberately allowed to
        # propagate: a broken jobs module is a bug, not an app without jobs.
        module = import_module(module_path)

        register = getattr(module, "register", None)
        if register is None:
            logger.warning(
                "%s has no register(scheduler) function, skipping it.", module_path
            )
            continue

        register(scheduler)
        registered.append(module_path)

    return registered
