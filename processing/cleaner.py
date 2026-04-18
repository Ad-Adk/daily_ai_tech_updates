def clean_articles(articles):
    cleaned = []
    
    for a in articles:
        if not a.get("title") or not a.get("description"):
            continue
        
        cleaned.append({
            "title": a["title"],
            "description": a["description"],
            "url": a["url"]
        })

    return cleaned

if __name__ == "__main__":
    sample_articles = [
        {"title": "AI breakthrough", "description": "New AI model achieves state-of-the-art results", "url": "http://example.com/ai-breakthrough"},
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