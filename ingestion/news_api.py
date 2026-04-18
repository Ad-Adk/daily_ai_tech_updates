import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import serpapi
from config.config import NEWS_API_KEY, TOPIC_TOKEN

client = serpapi.Client(api_key=NEWS_API_KEY)

def _get_article_link(article):
    if article.get("link"):
        return article["link"]

    stories = article.get("stories", [])
    if stories:
        return stories[0].get("link", "N/A")

    return "N/A"


def _get_article_source(article):
    if article.get("source"):
        return article["source"]

    stories = article.get("stories", [])
    if stories:
        return stories[0].get("source", "N/A")

    return "N/A"


def fetch_news():
    results = client.search({
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "topic_token": TOPIC_TOKEN
    })
    return results.get("news_results", [])


if __name__ == "__main__":
    news = fetch_news()

    for article in news:
        title = article.get("title", "N/A")
        link = _get_article_link(article)
        source = _get_article_source(article)

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Source: {source}")
        print("-" * 80)
