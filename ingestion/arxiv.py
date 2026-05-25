"""
arxiv.py – Fetch recent AI papers from the arXiv RSS/Atom feed.
"""

import feedparser


_ARXIV_URL = (
    "http://export.arxiv.org/api/query"
    "?search_query=ai&start=0&max_results=5"
)


def fetch_arxiv() -> list[dict]:
    """Return a list of {title, description, url} dicts from arXiv."""
    feed = feedparser.parse(_ARXIV_URL)
    return [
        {
            "title": entry.title,
            "description": entry.summary,
            "url": entry.link,
        }
        for entry in feed.entries
    ]


if __name__ == "__main__":
    for paper in fetch_arxiv():
        print(f"Title: {paper['title']}")
        print(f"URL:   {paper['url']}")
        print("-" * 80)
