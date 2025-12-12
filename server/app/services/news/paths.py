import os

BASE_SCRAPER_DIR = "app/scrapers/cryptoslate_scraper/scraped_articles"

UNPROCESSED_DIR = os.path.join(BASE_SCRAPER_DIR, "unprocessed")
PROCESSED_DIR = os.path.join(BASE_SCRAPER_DIR, "processed")
FAILED_DIR = os.path.join(BASE_SCRAPER_DIR, "failed")

# Ensure folders exist
os.makedirs(UNPROCESSED_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(FAILED_DIR, exist_ok=True)
