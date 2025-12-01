import os
from app.services.news.file_parser import parse_article_file

SCRAPED_DIR = "app/scrapers/cryptoslate_scraper/scraped_articles"


def load_all_scraped_articles():
    print("\n================= LOADING SCRAPED ARTICLES =================")
    print("SCRAPED_DIR =", SCRAPED_DIR)
    print("ABSOLUTE SCRAPED_DIR =", os.path.abspath(SCRAPED_DIR))

    articles = []

    if not os.path.isdir(SCRAPED_DIR):
        print("ERROR: Directory does not exist!")
        return articles

    files = os.listdir(SCRAPED_DIR)
    print("Found files:", files)

    for filename in files:
        print("\n--- Checking:", filename)

        if not filename.endswith(".txt"):
            print("Skipped (not .txt)")
            continue

        filepath = os.path.join(SCRAPED_DIR, filename)
        print("Full path:", filepath)

        parsed = parse_article_file(filepath)
        print("Parsed result:", parsed)

        # 🔥 Add filename + filepath so route doesn't break
        parsed["filename"] = filename
        parsed["filepath"] = filepath

        articles.append(parsed)

    print("TOTAL ARTICLES LOADED =", len(articles))
    print("============================================================\n")

    return articles
