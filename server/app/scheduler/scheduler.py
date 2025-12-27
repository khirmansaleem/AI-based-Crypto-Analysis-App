import asyncio
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from app.services.pipeline.daily_pipeline import process_daily_news


import asyncio
import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

# from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from app.services.pipeline.daily_pipeline import process_daily_news

logger = logging.getLogger(__name__)

# ✅ Blocking scheduler (systemd-safe, UTC-based)
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
    Start APScheduler.
    TEMPORARILY configured to run ONCE for testing.
    """

    scheduler.remove_all_jobs()

    # =====================================================
    # 🚫 DAILY CRON (TEMPORARILY DISABLED FOR TESTING)
    # =====================================================
    # trigger = CronTrigger(hour=22, minute=40)
    #
    # scheduler.add_job(
    #     _run_daily_news_pipeline,
    #     trigger=trigger,
    #     id="daily_news_pipeline",
    #     replace_existing=True,
    #     max_instances=1,
    #     misfire_grace_time=3600,  # 1 hour
    #     coalesce=True,
    # )

    # =====================================================
    # 🧪 ONE-TIME TEST RUN (runs once after 1 minute)
    # =====================================================
    test_trigger = DateTrigger(run_date=datetime.utcnow() + timedelta(minutes=1))

    scheduler.add_job(
        _run_daily_news_pipeline,
        trigger=test_trigger,
        id="daily_news_pipeline_test_once",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()
    logger.info("🧪 APScheduler started — one-time test job scheduled (UTC)")


def stop_scheduler():
    """
    Stop scheduler safely.
    """
    try:
        scheduler.shutdown(wait=False)
        logger.info("🛑 APScheduler shut down")
    except Exception as e:
        logger.error(f"❌ Error shutting down scheduler: {e}")
