"""
personalization.py – Score and rank articles by relevance and technical depth.
"""

from config.config import HIGH_VALUE_TOPICS, HIGH_VALUE_SKILLS, KEYWORDS

_KEYWORDS_LOWER = [k.lower() for k in KEYWORDS]
_LONG_SUMMARY   = 300
_MANY_SKILLS    = 4


def _score(article: dict) -> int:
    topic  = article.get("topic", "General")
    skills = article.get("skills", [])
    text   = (article.get("title", "") + " " + article.get("summary", "")).lower()

    score  = HIGH_VALUE_TOPICS.get(topic, 1)
    score += len(skills) * 2
    score += sum(HIGH_VALUE_SKILLS.get(s, 1) for s in skills)
    score += sum(2 for k in _KEYWORDS_LOWER if k in text)
    score += 2 if len(article.get("summary", "")) > _LONG_SUMMARY else 0
    score += 3 if len(skills) >= _MANY_SKILLS else 0
    return score


def rank_articles(articles: list[dict]) -> list[dict]:
    """Attach a numeric 'score' to each article and return them highest-first."""
    for article in articles:
        article["score"] = _score(article)
    return sorted(articles, key=lambda x: x["score"], reverse=True)


if __name__ == "__main__":
    _samples = [
        {"title": "AI breakthrough",       "summary": "New AI SOTA results",         "skills": ["LLM fine-tuning"]},
        {"title": "MLOps strategies",      "summary": "Deploying AI models",         "skills": ["MLOps"]},
        {"title": "Transformer deep-dive", "summary": "Latest transformer models",   "skills": ["Transformers"]},
        {"title": "General AI news",       "summary": "Latest AI updates",           "skills": []},
    ]
    for a in rank_articles(_samples):
        print(f"[{a['score']:3d}] {a['title']}")
