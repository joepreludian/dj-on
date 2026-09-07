import types
from unittest.mock import patch

from apscheduler.schedulers.blocking import BlockingScheduler
from base.scheduler import register_jobs
from django.core.management import get_commands


def make_scheduler() -> BlockingScheduler:
    """A stopped scheduler backed by the default in-memory store.

    Jobs added while stopped stay pending, and `get_jobs()` returns them, so the
    registration wiring can be asserted without touching the database or
    starting a process.
    """
    return BlockingScheduler(timezone="UTC")


class TestRegisterJobs:
    def test_registers_the_base_app_jobs(self):
        scheduler = make_scheduler()

        registered = register_jobs(scheduler)

        assert "base.jobs" in registered

    def test_registers_the_housekeeping_job_only_once(self):
        scheduler = make_scheduler()

        register_jobs(scheduler)

        job_ids = [job.id for job in scheduler.get_jobs()]
        assert job_ids == ["base.delete_old_job_executions"]

    def test_skips_installed_apps_without_a_jobs_module(self):
        scheduler = make_scheduler()

        registered = register_jobs(scheduler)

        # django_apscheduler, admin, auth and friends are all installed and none
        # of them declare jobs.
        assert registered == ["base.jobs"]

    def test_skips_a_jobs_module_without_a_register_function(self):
        scheduler = make_scheduler()
        app_config = types.SimpleNamespace(name="stub_app", module=object())

        with (
            patch("base.scheduler.apps.get_app_configs", return_value=[app_config]),
            patch("base.scheduler.module_has_submodule", return_value=True),
            patch("base.scheduler.import_module", return_value=object()),
        ):
            registered = register_jobs(scheduler)

        assert registered == []
        assert scheduler.get_jobs() == []


class TestRunApschedulerCommand:
    def test_command_is_discoverable(self):
        assert "run_apscheduler" in get_commands()
