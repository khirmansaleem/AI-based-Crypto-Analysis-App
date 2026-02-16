import os
import re
import time
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser
from datetime import datetime, timezone, timedelta
from app.services.news.paths import UNPROCESSED_DIR

CATEGORIES = {
    "regulation": 3,
    "etf": 2,
    "macro": 3,
    "exchanges": 3,
    "investments": 2,
    "stablecoins": 2,
}

MAX_ARTICLE_AGE_DAYS = 14

BASE_URL = "https://cryptoslate.com/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

OUTPUT_FOLDER = UNPROCESSED_DIR
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)

# -----------------------------
# Helpers
# -----------------------------
from datetime import datetime, timezone, timedelta


def is_within_days(published_at: str, max_days: int) -> bool:
    try:
        published_dt = dateparser.parse(published_at)
        if not published_dt:
            return False

        if published_dt.tzinfo is None:
            published_dt = published_dt.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        return (now - published_dt) <= timedelta(days=max_days)
    except Exception:
        return False


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_\-\. ]+", "", name)
    return name.strip().replace(" ", "_")[:120]


def get_heading_text(category: str) -> str:
    return {
        "regulation": "Regulation News",
        "etf": "ETF News",
        "macro": "Macro News",
        "exchanges": "Exchanges News",
        "investments": "Investments News",
        "stablecoins": "Stablecoins News",
    }.get(category, f"{category.capitalize()} News")


def looks_like_title(text: str) -> bool:
    text = " ".join(text.split())
    if len(text) < 30:
        return False
    if len(text.split()) < 4:
        return False
    if "News" in text or "Subscribe" in text:
        return False
    return True


def safe_get(url: str, max_retries: int = 3, timeout: int = 15):
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=timeout)
        except requests.RequestException:
            if attempt == max_retries - 1:
                return None
        else:
            if resp.status_code in (403, 429):
                return None
            if resp.status_code == 200:
                return resp

        time.sleep((2**attempt) + random.uniform(0.0, 1.0))

    return None


# -----------------------------
# Published date extractor
# -----------------------------
def fetch_published_date(soup: BeautifulSoup) -> str:
    time_tag = soup.find("time", attrs={"datetime": True})
    if time_tag and time_tag.get("datetime"):
        return time_tag["datetime"].strip()

    meta_time = soup.find("meta", {"property": "article:published_time"})
    if meta_time and meta_time.get("content"):
        return meta_time["content"].strip()

    post_date_div = soup.find("div", class_="post-date")
    if post_date_div:
        try:
            raw_text = post_date_div.get_text(" ", strip=True)
            dt = dateparser.parse(raw_text, fuzzy=True)
            return dt.isoformat()
        except Exception:
            pass

    return ""


# -----------------------------
# Full article fetch
# -----------------------------
def fetch_full_article(url: str) -> tuple[str, str]:
    time.sleep(random.uniform(1.5, 3.5))

    resp = safe_get(url)
    if resp is None:
        return "CONTENT_FETCH_FAILED", ""

    soup = BeautifulSoup(resp.text, "html.parser")

    selectors = [
        "div.single__content-wrap p",
        "div.single__content p",
        "article.page-article p",
        "article p",
    ]

    content = "NO_CONTENT_FOUND"
    for sel in selectors:
        paragraphs = soup.select(sel)
        if paragraphs:
            content = "\n".join(p.get_text(strip=True) for p in paragraphs)
            break

    published_at = fetch_published_date(soup)
    return content, published_at


# -----------------------------
# Category listing scraper
# -----------------------------
def scrape_top_news(limit: int = 15):
    url = "https://cryptoslate.com/top-news/"
    resp = safe_get(url)
    if resp is None:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    articles = []
    seen = set()

    # Target 24h panel
    panel = soup.find("section", id="top-news-panel-24h")
    if not panel:
        return []

    for article in panel.select("article.top-news-article"):
        link = article.find("a", class_="top-news-link", href=True)
        if not link:
            continue

        href = link["href"]
        if href in seen:
            continue
        seen.add(href)

        title = link.get("title") or link.get_text(strip=True)
        if not title:
            continue

        articles.append(
            {
                "category": "top-news",
                "title": title.strip(),
                "url": href,
                "published_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        if len(articles) >= limit:
            break

    return articles


# -----------------------------
# MAIN SCRAPER FUNCTION
# -----------------------------
def scrape_latest_news() -> int:
    total_saved = 0

    articles = scrape_top_news(limit=15)

    for art in articles:
        content, published_at = fetch_full_article(art["url"])

        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        filename = f"topnews__{sanitize_filename(art['title'])}__{ts}.txt"
        path = os.path.join(OUTPUT_FOLDER, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Category: Top News\n")
            f.write(f"Title: {art['title']}\n")
            f.write(f"URL: {art['url']}\n")
            f.write(f"PublishedAt: {published_at}\n")
            f.write("\n" + "=" * 80 + "\n\n")
            f.write(content)

        total_saved += 1
        time.sleep(random.uniform(1.0, 2.0))

    return total_saved


if __name__ == "__main__":
    print("Starting manual scraper test...")
    count = scrape_latest_news()
    print(f"Scraping finished. Saved {count} articles.")
