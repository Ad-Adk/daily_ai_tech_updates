def extract_insights(article):
    text = article["description"].lower()

    skills = []
    topic = "General"

    if "llm" in text or "gpt" in text:
        topic = "LLM"
        skills += ["Fine-tuning", "Prompt Engineering"]
    elif "vision" in text:
        topic = "Computer Vision"
        skills += ["CNN", "OpenCV"]
    elif "deployment" in text:
        topic = "MLOps"
        skills += ["Docker", "CI/CD"]

    return {
        "title": article["title"],
        "summary": article["description"],
        "topic": topic,
        "skills": list(set(skills)),
        "url": article["url"]
    }

if __name__ == "__main__":
    sample_article = {
        "title": "New LLM breakthrough",
        "description": "A new LLM model achieves state-of-the-art results in NLP tasks.",
        "url": "http://example.com/llm-breakthrough"
    }

    insights = extract_insights(sample_article)
    print(f"Title: {insights['title']}")
    print(f"Summary: {insights['summary']}")
    print(f"Topic: {insights['topic']}")
    print(f"Skills to Learn: {', '.join(insights['skills'])}")
    print(f"URL: {insights['url']}")