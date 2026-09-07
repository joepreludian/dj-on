"""Scheduled jobs owned by the `base` app.

Copy this shape into any app that needs scheduled work: define the callables,
then register them in `register(scheduler)`. `base.scheduler.register_jobs`
discovers the module automatically, so the management command never changes.
"""

import logging

from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler.util import close_old_connections

logger = logging.getLogger(__name__)


@close_old_connections
def delete_old_job_executions() -> None:
    """Prune execution history so django_apscheduler's table stops growing."""
    max_age = settings.APSCHEDULER_JOB_EXECUTIONS_MAX_AGE
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
    logger.info("Deleted job executions older than %s seconds.", max_age)


def register(scheduler) -> None:
    """Add this app's jobs to the scheduler."""
    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
        id="base.delete_old_job_executions",
        max_instances=1,
        replace_existing=True,
    )

    # The scheduler is a single process that cannot be scaled: a slow job here
    # delays every other job. Schedule the enqueue, not the work itself.
    #
    #     from base.tasks import send_daily_report
    #
    #     scheduler.add_job(
    #         send_daily_report.send,
    #         trigger=CronTrigger(hour="07", minute="30"),
    #         id="base.send_daily_report",
    #         max_instances=1,
    #         replace_existing=True,
    #     )
