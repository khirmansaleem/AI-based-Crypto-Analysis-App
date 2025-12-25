import asyncio
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.pipeline.daily_pipeline import process_daily_news

logger = logging.getLogger(__name__)

# ✅ Blocking scheduler (systemd-safe)
scheduler = BlockingScheduler(timezone="UTC")


def _run_daily_news_pipeline():
    """
    Wrapper to run async pipeline inside BlockingScheduler.
    """
    logger.info("🚀 Starting daily news pipeline")
    asyncio.run(process_daily_news())
    logger.info("✅ Daily news pipeline completed")


def start_scheduler():
    """
    Start APScheduler with daily cron job (UTC).
    """

    scheduler.remove_all_jobs()

    trigger = CronTrigger(hour=23, minute=10)  # 00:50 UTC daily

    scheduler.add_job(
        _run_daily_news_pipeline,
        trigger=trigger,
        id="daily_news_pipeline",
        replace_existing=True,
        max_instances=1,
        misfire_grace_time=3600,  # 1 hour
        coalesce=True,
    )

    scheduler.start()
    logger.info("🕒 APScheduler started — daily job at 00:50 UTC")


def stop_scheduler():
    """
    Stop scheduler safely.
    """
    try:
        scheduler.shutdown(wait=False)
        logger.info("🛑 APScheduler shut down")
    except Exception as e:
        logger.error(f"❌ Error shutting down scheduler: {e}")
