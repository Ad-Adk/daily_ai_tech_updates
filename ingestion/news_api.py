import os
import sys
import requests
from bs4 import BeautifulSoup
import serpapi

from pathlib import Path
from dotenv import load_dotenv

# Locate config/.env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

# Export variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TOPIC_TOKEN = os.getenv("TOPIC_TOKEN")
client = serpapi.Client(api_key=NEWS_API_KEY)

def _get_article_link(article):
    if article.get("link"):
        return article["link"]

    stories = article.get("stories", [])
    if stories:
        return stories[0].get("link", None)

    return None

def _get_article_description(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all paragraph text
        paragraphs = soup.find_all("p")

        content = " ".join(
            p.get_text(strip=True)
            for p in paragraphs
            if p.get_text(strip=True)
        )

        # Optional: limit size
        return content[:3000] if content else None

    except Exception:
        return None


def fetch_news():
    results = client.search({
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "topic_token": TOPIC_TOKEN
    })

    news=[]
    news_articles = results.get("news_results", [])[:20]
    for article in news_articles:
        news.append({
            "title": article.get("title", None),
            "url": _get_article_link(article),
            "description": _get_article_description(_get_article_link(article))
        })

    return news

if __name__ == "__main__":
    news = fetch_news()

    for article in news:
        print(f"Title: {article['title']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print("-" * 80)