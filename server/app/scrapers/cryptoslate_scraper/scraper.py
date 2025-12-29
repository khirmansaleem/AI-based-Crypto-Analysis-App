import os
import re
import time
import random
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Tag
from dateutil import parser as dateparser

from app.services.news.paths import UNPROCESSED_DIR


# -----------------------------
# Tier S Categories + Limits
# -----------------------------
# CATEGORIES = {
#    "regulation": 3,
#    "etf": 2,
#    "macro": 3,
#    "exchanges": 3,
#    "investments": 2,
#    "stablecoins": 2,
# }


CATEGORIES = {
    "regulation": 3,
    "etf": 2,
    "macro": 1,
    "exchanges": 3,
    "investments": 2,
    "stablecoins": 2,
}

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

# Create directories if missing
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


session = requests.Session()
session.headers.update(HEADERS)


# -----------------------------
# Helpers
# -----------------------------
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

        sleep_sec = (2**attempt) + random.uniform(0.0, 1.0)
        time.sleep(sleep_sec)

    return None


# -----------------------------
# Published date extractor
# -----------------------------


def fetch_published_date(soup: BeautifulSoup) -> str:
    """
    Extracts the published date from a CryptoSlate article page.
    Returns ISO-8601 timestamp like '2025-12-08T18:45:00+00:00'
    """

    # 1. Preferred: <time datetime="...">
    time_tag = soup.find("time", attrs={"datetime": True})
    if time_tag and time_tag.get("datetime"):
        return time_tag["datetime"].strip()

    # 2. Meta tag fallback (rare but valid)
    meta_time = soup.find("meta", {"property": "article:published_time"})
    if meta_time and meta_time.get("content"):
        return meta_time["content"].strip()

    # 3. Fallback: <div class="post-date"> Dec. 8, 2025 at 6:45 pm UTC
    post_date_div = soup.find("div", class_="post-date")
    if post_date_div:
        try:
            # Extract date + time together
            raw_text = post_date_div.get_text(" ", strip=True)

            # Example: "Dec. 8, 2025 at 6:45 pm UTC"
            dt = dateparser.parse(raw_text, fuzzy=True)
            return dt.isoformat()

        except Exception:
            pass

    return ""  # No date found


# -----------------------------
# Full article fetch
# -----------------------------
def fetch_full_article(url: str) -> tuple[str, str]:
    """
    Returns: (content, published_at)
    """
    time.sleep(random.uniform(1.5, 3.5))

    resp = safe_get(url)
    if resp is None:
        return "CONTENT_FETCH_FAILED", ""

    soup = BeautifulSoup(resp.text, "html.parser")

    # --- extract content ---
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

    # --- extract published date ---
    published_at = fetch_published_date(soup)

    return content, published_at


# -----------------------------
# Category listing scraper (SMART VERSION)
# Picks the most recent articles based on published date
# -----------------------------
def scrape_listing(category: str, limit: int):
    url = BASE_URL + category + "/"

    time.sleep(random.uniform(2.0, 4.0))

    resp = safe_get(url)
    if resp is None:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    heading_text = get_heading_text(category)
    heading_tag = soup.find(
        lambda tag: isinstance(tag, Tag)
        and tag.name in ("h1", "h2")
        and heading_text in tag.get_text(strip=True)
    )

    if not heading_tag:
        return []

    articles = []
    seen_urls = set()

    # Instead of stopping early, collect MANY links
    # (The listing page may have mixed old/new items)
    for link in heading_tag.find_all_next("a", href=True):
        title = link.get_text(strip=True)
        if not looks_like_title(title):
            continue

        href = link["href"]
        if href.startswith("/"):
            href = "https://cryptoslate.com" + href

        if "cryptoslate.com" not in href:
            continue

        if href in seen_urls:
            continue

        seen_urls.add(href)

        # Fetch published date using lightweight request
        preview_resp = safe_get(href)
        if preview_resp is None:
            continue

        preview_soup = BeautifulSoup(preview_resp.text, "html.parser")
        published_at = fetch_published_date(preview_soup)

        # Ignore items without dates
        if not published_at:
            continue

        articles.append(
            {
                "category": category,
                "title": title,
                "url": href,
                "published_at": published_at,
            }
        )

        # Still keep going — we want enough candidates to sort

    # Sort newest → oldest
    articles.sort(key=lambda x: x["published_at"], reverse=True)

    # Return only the top N most recent
    return articles[:limit]


# -----------------------------
# MAIN SCRAPER FUNCTION (for pipeline)
# -----------------------------
def scrape_latest_news() -> int:
    """
    Scrapes each category, selects MOST RECENT articles based on published date,
    saves them into TXT files, and returns the total count.
    """
    total_saved = 0

    for category, limit in CATEGORIES.items():
        articles = scrape_listing(category, limit)

        for art in articles:
            content, published_at = fetch_full_article(art["url"])

            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            filename = f"{category}__{sanitize_filename(art['title'])}__{ts}.txt"
            path = os.path.join(OUTPUT_FOLDER, filename)

            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Category: {art['category']}\n")
                f.write(f"Title: {art['title']}\n")
                f.write(f"URL: {art['url']}\n")
                f.write(f"PublishedAt: {published_at}\n")
                f.write("\n" + "=" * 80 + "\n\n")
                f.write(content)

            total_saved += 1
            time.sleep(random.uniform(1.0, 2.5))

        time.sleep(random.uniform(2.0, 4.0))

    return total_saved


if __name__ == "__main__":
    print("Starting manual scraper test...")
    count = scrape_latest_news()
    print(f"Scraping finished. Saved {count} articles.")
