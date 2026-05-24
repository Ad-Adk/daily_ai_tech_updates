import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import HIGH_VALUE_TOPICS, HIGH_VALUE_SKILLS, KEYWORDS 

def rank_articles(articles):
    
    for article in articles:
        score = 0

        topic = article.get("topic", "General")
        skills = article.get("skills", [])
        text = (
            article.get("title", "") + " " +
            article.get("summary", "")
        ).lower()

        # Topic importance
        score += HIGH_VALUE_TOPICS.get(topic, 1)

        # Skill count
        score += len(skills) * 2

        # Valuable skills
        for skill in skills:
            score += HIGH_VALUE_SKILLS.get(skill, 1)

        # Trending AI keywords
        for keyword in KEYWORDS:
            if keyword in text:
                score += 2

        # Bonus for deeper technical articles
        if len(article.get("summary", "")) > 300:
            score += 2

        # Bonus for many technical skills
        if len(skills) >= 4:
            score += 3

        article["score"] = score

    return sorted(
        articles,
        key=lambda x: x["score"],
        reverse=True
    )

if __name__ == "__main__":
    sample_articles = [
        {"title": "AI breakthrough", "description": "New AI model achieves state-of-the-art results", "url": "http://example.com/ai-breakthrough", "skills": ["Learn LLM fine-tuning"]},
        {"title": "MLOps strategies", "description": "Best practices for deploying AI models", "url": "http://example.com/mlops-strategies", "skills": ["Learn MLOps"]},
        {"title": "Transformer architectures", "description": "Understanding the latest transformer models", "url": "http://example.com/transformer-architectures", "skills": ["Understand Transformers"]},
        {"title": "General AI news", "description": "Latest updates in AI technology", "url": "http://example.com/general-ai-news", "skills": []}
    ]

    ranked = rank_articles(sample_articles)
    for article in ranked:
        print(f"Title: {article['title']}")
        print(f"Skills: {', '.join(article['skills'])}")
        print(f"Score: {article['score']}")
        print("-" * 80)