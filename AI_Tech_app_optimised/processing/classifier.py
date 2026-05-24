"""
classifier.py – Filter articles to those relevant to AI/tech topics.
"""

from config.config import KEYWORDS

# Pre-lowercase keywords once at import time for fast repeated lookups
_KEYWORDS_LOWER = [k.lower() for k in KEYWORDS]


def filter_relevant(articles: list[dict]) -> list[dict]:
    """Return only articles whose title+description match at least one keyword."""
    return [
        a for a in articles
        if any(k in (a["title"] + " " + a["description"]).lower()
               for k in _KEYWORDS_LOWER)
    ]


if __name__ == "__main__":
    _samples = [
        {"title": "AI breakthrough",   "description": "New LLM achieves SOTA",           "url": "http://example.com/1"},
        {"title": "Sports update",     "description": "Local team wins championship",     "url": "http://example.com/2"},
        {"title": "MLOps strategies",  "description": "Deploy ML models effectively",    "url": "http://example.com/3"},
        {"title": "Cooking tips",      "description": "How to make the perfect pasta",   "url": "http://example.com/4"},
    ]
    for a in filter_relevant(_samples):
        print(f"✓ {a['title']}")
