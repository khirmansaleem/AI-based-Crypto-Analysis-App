import os
import re
import time
import random
from datetime import datetime

import requests
from bs4 import BeautifulSoup, Tag

# -----------------------------
# Tier S Categories + Limits
# -----------------------------
CATEGORIES = {
    "regulation": 3,
    "etf": 2,
    "macro": 3,
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

OUTPUT_FOLDER = "scraped_articles"
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
    """
    Safe GET with small retry + backoff.
    If we see 403/429, stop and return None.
    """
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=timeout)
        except requests.RequestException:
            # connection / DNS / timeout errors
            if attempt == max_retries - 1:
                return None
            # backoff on next loop
        else:
            if resp.status_code in (403, 429):
                # forbidden or too many requests: do not hammer
                return None
            if resp.status_code == 200:
                return resp

        # backoff before retry
        sleep_sec = (2**attempt) + random.uniform(0.0, 1.0)
        time.sleep(sleep_sec)

    return None


# -----------------------------
# Full article fetch
# -----------------------------
def fetch_full_article(url: str) -> str:
    # simulate human delay before reading a page
    time.sleep(random.uniform(1.5, 3.5))

    resp = safe_get(url)
    if resp is None:
        return "CONTENT_FETCH_FAILED"

    soup = BeautifulSoup(resp.text, "html.parser")

    selectors = [
        "div.single__content-wrap p",
        "div.single__content p",
        "article.page-article p",
        "article p",
    ]

    for sel in selectors:
        paragraphs = soup.select(sel)
        if paragraphs:
            return "\n".join(p.get_text(strip=True) for p in paragraphs)

    return "NO_CONTENT_FOUND"


# -----------------------------
# Stable Article Listing Scraper
# -----------------------------
def scrape_listing(category: str, limit: int):
    url = BASE_URL + category + "/"

    # simulate human delay before hitting a category page
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

    for link in heading_tag.find_all_next("a", href=True):
        if len(articles) >= limit:
            break

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

        articles.append(
            {
                "category": category,
                "title": title,
                "url": href,
            }
        )

    return articles


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    total_saved = 0

    # if you want, you can randomize category order each day:
    # import random
    # items = list(CATEGORIES.items())
    # random.shuffle(items)
    # for category, limit in items:
    for category, limit in CATEGORIES.items():
        articles = scrape_listing(category, limit)

        for art in articles:
            content = fetch_full_article(art["url"])

            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
            filename = f"{category}__{sanitize_filename(art['title'])}__{ts}.txt"
            path = os.path.join(OUTPUT_FOLDER, filename)

            with open(path, "w", encoding="utf-8") as f:
                f.write(f"Category: {art['category']}\n")
                f.write(f"Title: {art['title']}\n")
                f.write(f"URL: {art['url']}\n")
                f.write("\n" + "=" * 80 + "\n\n")
                f.write(content)

            total_saved += 1

            # delay between saving articles (looks like reading time)
            time.sleep(random.uniform(1.0, 2.5))

        # small pause before next category
        time.sleep(random.uniform(2.0, 4.0))

    print(f"\n[DONE] Saved {total_saved} articles into '{OUTPUT_FOLDER}'")
