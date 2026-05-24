import re
def clean_text(text):
    # Keep letters, numbers, spaces, and basic punctuation
    text = re.sub(r"[^A-Za-z0-9\s.,!?:'-]", '', text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_articles(articles):
    cleaned = []

    for a in articles:
        title = a.get("title")
        description = a.get("description")

        # Use 'url' if available, otherwise fallback to 'link'
        url = a.get("url") or a.get("link")

        if not title or not description or not url:
            continue

        cleaned.append({
            "title": clean_text(title),
            "description": clean_text(description),
            "url": url
        })

    return cleaned

if __name__ == "__main__":
    sample_articles = [
        {"title": "AI breakthrough", "description": "New AI model achieves state-of-the-art results", "link": "http://example.com/ai-breakthrough"},
        {"title": "", "description": "Missing title", "url": "http://example.com/missing-title"},
        {"title": "Missing description", "description": "", "url": "http://example.com/missing-description"},
        {"title": "Valid article", "description": "This article has all fields", "url": "http://example.com/valid-article"}
    ]

    cleaned = clean_articles(sample_articles)
    for article in cleaned:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print("-" * 80)