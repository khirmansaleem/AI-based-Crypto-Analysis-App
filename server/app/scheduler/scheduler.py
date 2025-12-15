from apscheduler.triggers.cron import CronTrigger
from app.services.pipeline.daily_pipeline import process_daily_news
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger(__name__)

# Use AsyncIOScheduler instead of BackgroundScheduler
scheduler = AsyncIOScheduler()


def start_scheduler():
    """
    Start the APScheduler with a daily cron job that supports async functions.
    Runs after FastAPI starts.
    """

    scheduler.remove_all_jobs()

    trigger = CronTrigger(hour=3, minute=14)

    scheduler.add_job(
        process_daily_news,  # async function ✔
        trigger=trigger,
        id="daily_news_pipeline",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=3600,
    )

    scheduler.start()
    logger.info("APScheduler started with daily job at 03:06 AM")


def stop_scheduler():
    """
    Stop scheduler safely when FastAPI shuts down.
    """
    try:
        scheduler.shutdown()
        logger.info("APScheduler shut down")
    except Exception as e:
        logger.error(f"Error shutting down scheduler: {e}")
