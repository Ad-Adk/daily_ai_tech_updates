"""
cleaner.py – Strip noise from raw article text and filter incomplete records.
"""

import re

_ALLOWED = re.compile(r"[^A-Za-z0-9\s.,!?:'\-]")
_SPACES  = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Remove non-standard characters and collapse whitespace."""
    text = _ALLOWED.sub("", text)
    return _SPACES.sub(" ", text).strip()


def clean_articles(articles: list[dict]) -> list[dict]:
    """
    Normalise and validate a list of raw article dicts.
    Articles missing title, description, or URL are silently dropped.
    """
    cleaned = []
    for a in articles:
        title       = a.get("title")
        description = a.get("description")
        url         = a.get("url") or a.get("link")   # support both key names

        if not (title and description and url):
            continue

        cleaned.append({
            "title":       clean_text(title),
            "description": clean_text(description),
            "url":         url,
        })
    return cleaned


if __name__ == "__main__":
    _samples = [
        {"title": "AI breakthrough",   "description": "New AI model achieves SOTA!", "link": "http://example.com/1"},
        {"title": "",                  "description": "Missing title",               "url":  "http://example.com/2"},
        {"title": "Valid article",     "description": "All fields present",          "url":  "http://example.com/3"},
    ]
    for a in clean_articles(_samples):
        print(f"Title: {a['title']} | URL: {a['url']}")
