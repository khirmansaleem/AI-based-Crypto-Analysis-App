from apscheduler.triggers.cron import CronTrigger
from app.services.pipeline.daily_pipeline import process_daily_news
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


logger = logging.getLogger(__name__)

# ✅ Explicit UTC scheduler
scheduler = AsyncIOScheduler()


def start_scheduler():
    """
    Start the APScheduler with a daily cron job (UTC).
    Runs after FastAPI starts.
    """

    scheduler.remove_all_jobs()

    # ✅ Daily at 12:30 AM
    trigger = CronTrigger(
        hour=0,
        minute=50,
    )
    scheduler.add_job(
        process_daily_news,  # async function ✔
        trigger=trigger,
        id="daily_news_pipeline",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=3600,  # 1 hour
        coalesce=True,  # combine missed runs
    )

    scheduler.start()
    logger.info("🕒 APScheduler started — daily job at 03:30 UTC")


def stop_scheduler():
    """
    Stop scheduler safely when FastAPI shuts down.
    """
    try:
        scheduler.shutdown(wait=False)
        logger.info("🛑 APScheduler shut down")
    except Exception as e:
        logger.error(f"❌ Error shutting down scheduler: {e}")
