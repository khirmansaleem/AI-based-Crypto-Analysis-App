import time

from app.scheduler.scheduler import start_scheduler, stop_scheduler


if __name__ == "__main__":
    print("🚀 Scheduler started as standalone process")
    start_scheduler()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
    finally:
        stop_scheduler()
        print("🛑 Scheduler stopped")
