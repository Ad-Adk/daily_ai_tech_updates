def rank_articles(articles):
    # simple scoring (can upgrade later)
    for a in articles:
        a["score"] = len(a.get("skills", []))

    return sorted(articles, key=lambda x: x["score"], reverse=True)

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