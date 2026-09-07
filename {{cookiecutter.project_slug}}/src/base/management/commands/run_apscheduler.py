import logging
import signal

from django.core.management.base import BaseCommand

from base.scheduler import create_scheduler, register_jobs

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run the scheduler process that executes this project's scheduled jobs."

    def handle(self, *args, **options):
        scheduler = create_scheduler()

        for module_path in register_jobs(scheduler):
            logger.info("Registered jobs from %s", module_path)

        # Docker stops containers with SIGTERM. Without this the scheduler would
        # ignore it and wait out the grace period before being killed.
        signal.signal(signal.SIGTERM, lambda *_: scheduler.shutdown())

        # These go through logging rather than self.stdout so that they interleave
        # correctly with APScheduler's own log records. Python block-buffers stdout
        # when it is not a TTY, which would otherwise reorder them in container logs.
        logger.info("Starting scheduler...")
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()

        logger.info("Scheduler stopped.")
