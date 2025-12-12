def parse_article_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()

    # Required fields
    category = lines[0].replace("Category: ", "").strip()
    title = lines[1].replace("Title: ", "").strip()
    url = lines[2].replace("URL: ", "").strip()

    # Optional PublishedAt field
    published_at = ""
    if lines[3].startswith("PublishedAt:"):
        published_at = lines[3].replace("PublishedAt:", "").strip()

    else:
        # backward compatibility if old files exist
        published_at = ""

    # Find the divider location ========
    divider_index = text.index("=" * 80)

    # Content starts after the divider line
    content = text[divider_index + 80 :].strip()

    return {
        "category": category,
        "title": title,
        "url": url,
        "published_at": published_at,  # <-- NEW FIELD
        "content": content,
    }
