import json
import os
from langchain_groq import ChatGroq
from pathlib import Path
from dotenv import load_dotenv

# Locate config/.env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

# Export variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

def extract_insights(article):
    text = article["description"]

    prompt = f"""
        You are an AI news analyst.

        Analyze the following article and return ONLY valid JSON.

        Required JSON format:
        {{
            "topic": "short category",
            "skills": ["skill1", "skill2"]
        }}

        Rules:
        - Topic should be concise related to AI/tech (e.g. LLM, Computer Vision, MLOps)
        - Skills should be technical skills/tools/concepts
        - Return max 5 skills
        - No markdown
        - No explanation
        - Output ONLY JSON

        Article:
        {text}
        """.strip()

    try:
        response = llm.invoke(prompt)

        content = response.content.strip()

        # Remove accidental markdown fences
        content = content.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(content)

        return {
            "title": article["title"],
            "summary": article["description"],
            "topic": parsed.get("topic", "General"),
            "skills": parsed.get("skills", []),
            "url": article["url"]
        }

    except Exception as e:
        print(f"Insight extraction error: {e}")

        return {
            "title": article["title"],
            "summary": article["description"],
            "topic": "General",
            "skills": [],
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