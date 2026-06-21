from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from app.database import engine
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def get_scheduler():
    """Create and configure APScheduler instance."""
    jobstores = {
        "default": SQLAlchemyJobStore(engine=engine)
    }

    executors = {
        "default": {
            "type": "threadpool",
            "max_workers": 5,
        }
    }

    job_defaults = {
        "coalesce": False,
        "max_instances": 1,
    }

    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=settings.scheduler_timezone,
    )

    return scheduler


def start_scheduler():
    """Start the background scheduler."""
    try:
        scheduler = get_scheduler()

        from app.scheduler.jobs import email_fetch_job, email_extraction_job

        scheduler.add_job(
            email_fetch_job.fetch_emails_for_all_users,
            "interval",
            hours=1,
            id="email_fetch_hourly",
            name="Fetch emails from Gmail hourly",
            replace_existing=True,
        )

        scheduler.add_job(
            email_extraction_job.process_unprocessed_emails,
            "interval",
            minutes=15,
            id="email_extraction_periodic",
            name="Process unprocessed emails",
            replace_existing=True,
        )

        scheduler.start()
        logger.info("Scheduler started successfully")
        return scheduler

    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        raise
