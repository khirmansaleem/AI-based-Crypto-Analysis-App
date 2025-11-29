def parse_article_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()

    category = lines[0].replace("Category: ", "").strip()
    title = lines[1].replace("Title: ", "").strip()
    url = lines[2].replace("URL: ", "").strip()

    # Content starts after divider line
    divider_index = text.index("=" * 80)
    content = text[divider_index + 80 :].strip()

    return {
        "category": category,
        "title": title,
        "url": url,
        "content": content,
    }
