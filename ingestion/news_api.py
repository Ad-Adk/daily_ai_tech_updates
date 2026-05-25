"""
news_api.py – Fetch AI news via SerpApi (Google News engine).
Scrapes article body text for downstream summarisation.
"""

import os
import requests
import serpapi
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from config.config import ENV_PATH

load_dotenv(dotenv_path=ENV_PATH)

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TOPIC_TOKEN  = os.getenv("TOPIC_TOKEN")

_client = serpapi.Client(api_key=NEWS_API_KEY)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}
_MAX_CONTENT  = 3000
_MAX_ARTICLES = 20


def _get_article_link(article: dict) -> str | None:
    """Return the best available URL for a news article dict."""
    if link := article.get("link"):
        return link
    stories = article.get("stories", [])
    return stories[0].get("link") if stories else None


def _scrape_description(url: str | None) -> str | None:
    """
    Fetch `url` and extract visible paragraph text.
    Returns up to _MAX_CONTENT characters, or None on any failure.
    """
    if not url:
        return None
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        text = " ".join(
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if p.get_text(strip=True)
        )
        return text[:_MAX_CONTENT] or None
    except Exception:
        return None


def fetch_news() -> list[dict]:
    """Return up to _MAX_ARTICLES news items as {title, url, description} dicts."""
    results = _client.search({
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "topic_token": TOPIC_TOKEN,
    })

    articles = []
    for raw in results.get("news_results", [])[:_MAX_ARTICLES]:
        url = _get_article_link(raw)
        articles.append({
            "title":       raw.get("title"),
            "url":         url,
            "description": _scrape_description(url),
        })
    return articles


if __name__ == "__main__":
    for article in fetch_news():
        print(f"Title: {article['title']}")
        print(f"URL:   {article['url']}")
        print("-" * 80)
