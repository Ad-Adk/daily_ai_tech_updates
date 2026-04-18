import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import KEYWORDS

def filter_relevant(articles):
    filtered = []

    for a in articles:
        text = (a["title"] + " " + a["description"]).lower()
        
        if any(k.lower() in text for k in KEYWORDS):
            filtered.append(a)

    return filtered

if __name__ == "__main__":
    sample_articles = [
        {"title": "AI breakthrough", "description": "New AI model achieves state-of-the-art results", "url": "http://example.com/ai-breakthrough"},
        {"title": "Sports update", "description": "Local team wins championship", "url": "http://example.com/sports-update"},
        {"title": "MLOps best practices", "description": "How to deploy machine learning models effectively", "url": "http://example.com/mlops-best-practices"},
        {"title": "Cooking tips", "description": "How to make the perfect pasta", "url": "http://example.com/cooking-tips"}
    ]

    filtered = filter_relevant(sample_articles)
    for article in filtered:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print("-" * 80)